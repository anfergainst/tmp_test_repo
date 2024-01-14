/**
 * DevOps.click CUSTOM API for WordPress.
 * Clone/Update Real State Posts
 */

add_action( 'rest_api_init', function () {
    register_rest_route( 'devops/v1', '/create-from-template/', array(
        'methods' => 'POST',
        'callback' => 'create_from_template',
//         'permission_callback' => function () {
//             return current_user_can( 'edit_posts' );
//         }
	) );
} );

// formatted_key = formatted_key.replace('\u00e7', 'c').replace('\u00e3', 'a').replace('\u00fa', 'u').replace('\u00e1', 'a').replace('\u00e9', 'e').replace('\u00f3', 'o').replace('\u00f5', 'o').replace('\u00ea', 'e').replace('\u00ed', 'i').replace('\u00da', 'u').replace('\u00b2.', '- ').replace('\u00a0', '\n')
// formatted_key = formatted_key.replace(' m\n2', '').replace('\u00e9', 'e').replace('\u00b2', '²').replace('\u00ba', 'o').replace('\u00c1', 'A')
// formatted_key = formatted_key.replace('(', '').replace(')', '').replace('\n', '')
// formatted_key = formatted_key.replace('&#8364;', '€')

function process_replacements($content) {
    $replacements = array(
        "u002d" => "-",
        "\u00e7" => "ç",
        "\u00e3" => "á",
        "\u00fa" => "ú",
        "\u00b2" => "²",
        "\u00e9" => "e",
        "\u00ba" => "o",
        "\u00c1" => "Á",
        "&#8364" => "€",
        // "\u00a0" => "\n",
    );

    foreach ($replacements as $original => $replacement) {
        $content = str_replace($original, $replacement, $content);
    }

    return $content;
}

function get_post_by_title($title) {
    $args = array(
        'post_type'  => 'post', // or your custom post type if applicable
        'post_status' => 'any',
        'title' => $title,
        'posts_per_page' => 1,
    );

    $posts = get_posts($args);

    if ( $posts ) {
        return $posts[0]->ID;
    }

    return false;
}

// function update_post_meta_with_json($post_id, $meta_key, $meta_value) {
//     // If meta_value is a JSON string, use wp_slash to add extra escaping
//     if (is_string($meta_value) && is_json($meta_value)) {
//         $meta_value = wp_slash($meta_value);
//     }
//     update_post_meta($post_id, $meta_key, $meta_value);
// }

function get_media_id_from_url($image_url) {
    if (empty($image_url)) {
        return null; // Return null if the URL is empty
    }

    global $wpdb;
    $attachment_id = $wpdb->get_var($wpdb->prepare("SELECT ID FROM $wpdb->posts WHERE guid='%s'", $image_url));

    if ($attachment_id) {
        return $attachment_id; // Return the existing media ID
    } else {
        // Code to upload the media and return its new ID if needed
    }

    return null;
}

function create_from_template( $request ) {
    $post_data = $request->get_json_params();

    // Validate required parameters
    if ( ! isset( $post_data['template_post_id'], $post_data['title'], $post_data['api_address'], $post_data['api_data'] ) ) {
        return new WP_Error( 'missing_parameters', 'Missing parameters', array( 'status' => 400 ) );
    }

    // Fetch the template post and its meta data
    $template_post = get_post( $post_data['template_post_id'] );
    if ( ! $template_post ) {
        return new WP_Error( 'invalid_template_post', 'Template post not found', array( 'status' => 404 ) );
    }

    // Fetch meta data and custom fields from the template post
    $template_meta = get_post_meta( $post_data['template_post_id'] );
    $template_custom_meta = get_post_meta( $post_data['template_post_id'], 'post_spectra_custom_meta', true );
    $template_spectra_custom_meta = get_post_meta($post_data['template_post_id'], 'spectra_custom_meta', true);

    // Fetch and process API response
    $response = wp_remote_get( $post_data['api_address'] );
    if ( is_wp_error( $response ) ) {
        return $response;
    }
    $api_response_body = wp_remote_retrieve_body( $response );

    // Ensure UTF-8 encoding and decode HTML entities
    $api_response_body = mb_convert_encoding($api_response_body, 'UTF-8', mb_detect_encoding($api_response_body));
    $api_response_body = html_entity_decode($api_response_body, ENT_QUOTES, 'UTF-8');

    // // Fetch and process API response
    // $response = wp_remote_get( $post_data['api_address'] );
    // if ( is_wp_error( $response ) ) {
    //     return $response;
    // }
    // $api_response_body = wp_remote_retrieve_body( $response );

    // // Ensure UTF-8 encoding and decode HTML entities
    // $api_response_body = mb_convert_encoding($api_response_body, 'UTF-8', mb_detect_encoding($api_response_body));
    // $api_response_body = html_entity_decode($api_response_body, ENT_QUOTES, 'UTF-8');

    // // Process content with mustache replacements
    // $content = $template_post->post_content;
    // foreach ( $post_data['api_data'] as $key => $value ) {
    //     $content = str_replace( "{{{$key}}}", $value, $content );
    // }

    // Processing content with mustache replacements
    foreach ( $post_data['api_data'] as $key => $value ) {
        // Decode HTML entities for each value
        $value = html_entity_decode($value, ENT_QUOTES, 'UTF-8');
        $content = str_replace( "{{{$key}}}", $value, $content );
    }

    // For featured media
    $featured_media_id = get_media_id_from_url($post_data['featured_image']);


    $post_content_processed = process_content_replacements($content);

    // Prepare new post data
    $new_post_data = array(
        'post_title'    => $post_data['title'],
        'post_content'  => $post_content_processed,
        // 'post_excerpt'  => str_replace("u002d", "-", $template_post->post_excerpt),
        'post_excerpt'  => $template_post->post_excerpt,
        'post_author'   => $template_post->post_author,
        'post_status'   => 'publish',
        'post_type'     => $template_post->post_type,
        'post_format'   => get_post_format($template_post->ID),
        'ping_status'   => $template_post->ping_status,
        'featured_media'=> $featured_media_id,
        // More fields here...
    );

    // Conditionally add featured_media if it exists
    if ($featured_media_id) {
        $new_post_data['featured_media'] = $featured_media_id;
    }

    $existing_post_id = get_post_by_title($post_data['title']);

    if ( $existing_post_id ) {
        // Fetch the template post again
        $template_post = get_post( $post_data['template_post_id'] );
        if ( ! $template_post ) {
            return new WP_Error( 'invalid_template_post', 'Template post not found', array( 'status' => 404 ) );
        }

        // Prepare content with mustache replacements
        $content = $template_post->post_content;
        foreach ( $post_data['api_data'] as $key => $value ) {
            $content = str_replace( "{{{$key}}}", $value, $content );
        }

        // Prepare the update data
        $updated_post_data = array(
            'ID'           => $existing_post_id,
            'post_content' => str_replace("u002d", "-", $content), // Updated content from template
            // Add other fields you want to update here
        );

        // Update the post
        $updated_post_id = wp_update_post( $updated_post_data );

        // Update the meta fields
        foreach ($template_meta as $key => $values) {
            foreach ($values as $value) {
                update_post_meta( $updated_post_id, $key, $value );
            }
        }

        // $escaped_json = '{"key":"value with \\"escaped quotes\\""}';
        // update_post_meta( $id, 'double_escaped_json', wp_slash( $escaped_json ) );
        // $fixed = get_post_meta( $id, 'double_escaped_json', true );


        // Update the spectra custom meta fields for the new or updated post
        // $template_spectra_custom_meta = wp_slash(json_encode($template_spectra_custom_meta));
        // update_post_meta($post_id, 'spectra_custom_meta', $template_spectra_custom_meta);
        // Update the spectra custom meta fields for the new or updated post
        update_post_meta($post_id, 'spectra_custom_meta', $template_spectra_custom_meta);


        if ( is_wp_error( $updated_post_id ) ) {
            return new WP_Error( 'post_update_failed', 'Failed to update post', array( 'status' => 500 ) );
        }

        return array( 'message' => 'Post updated successfully!', 'post_id' => $updated_post_id );
    } else {
        // Post does not exist, create it
        // ... [existing code to create a new post]

        // Get the ID of the newly created post
        $new_post_id = wp_insert_post( $new_post_data );

        // Update the meta fields for the new post
        foreach ($template_meta as $key => $values) {
            foreach ($values as $value) {
                update_post_meta( $new_post_id, $key, $value );
            }
        }

        // Update the spectra custom meta fields for the new or updated post
        update_post_meta($post_id, 'spectra_custom_meta', $template_spectra_custom_meta);
    }
}

/**
 * Not used yet
 */

function update_existing_post_mustache_values( $request ) {
    $post_data = $request->get_json_params();

    // Validate required parameters
    if ( ! isset( $post_data['template_post_id'], $post_data['title'], $post_data['api_address'], $post_data['api_data'] ) ) {
        return new WP_Error( 'missing_parameters', 'Missing parameters', array( 'status' => 400 ) );
    }

    // Fetch the template post
    $template_post = get_post( $post_data['template_post_id'] );
    if ( ! $template_post ) {
        return new WP_Error( 'invalid_post', 'Template post not found', array( 'status' => 404 ) );
    }

    // Connect to external API - Customize this part as per your API's requirements
    $response = wp_remote_get( $post_data['api_address'] );
    if ( is_wp_error( $response ) ) {
        return $response;
    }

    // Process content with mustache replacements
    $content = $template_post->post_content;
    foreach ( $post_data['api_data'] as $key => $value ) {
        $content = str_replace( "{{{$key}}}", $value, $content );
    }

    // Prepare new post data
    $new_post_data = array(
        'post_title'                    => $post_data['title'],
        'post_content'                  => $content,
        'post_excerpt'                  => $template_post->post_excerpt,
        'post_author'                   => $template_post->post_author,
        // More fields here...
        'post_status'                   => 'publish',
    );

    $existing_post_id = get_post_by_title($post_data['title']);

    if ( $existing_post_id ) {
        // Fetch existing post
        $existing_post = get_post($existing_post_id);

        // Prepare content with mustache replacements (similar to how you do it for new posts)
        $content = $existing_post->post_content;
        foreach ( $post_data['api_data'] as $key => $value ) {
            $content = str_replace( "{{{$key}}}", $value, $content );
        }

        // Prepare the update data
        $updated_post_data = array(
            'ID'           => $existing_post_id,
            'post_content' => $content, // Only updating the content
            // Add other fields you want to update here
        );

        // Update the post
        $updated_post_id = wp_update_post( $updated_post_data );

        if ( is_wp_error( $updated_post_id ) ) {
            return new WP_Error( 'post_update_failed', 'Failed to update post', array( 'status' => 500 ) );
        }

        return array( 'message' => 'Post updated successfully!', 'post_id' => $updated_post_id );
    } else {
        // Post does not exist, create it
        // ... [existing code to create a new post]
    }
}









// add_action( 'rest_api_init', function () {
//     error_log( 'Action rest_api_init just started' );

//    register_rest_route( 'meuapp/v1', '/clone-post/', array(
//       'methods' => 'POST',
//       'callback' => 'clone_post_function',
//       'permission_callback' => function () {
//          return current_user_can( 'edit_posts' );
//       }
//    ));
// 	error_log( 'Action rest_api_init just finished' );
// });

// function clone_post_function( $request ) {
// 	error_log( 'Function clone_post_function just started' );
//    $source_post_id = $request['source_post_id'];
//    $original_post = get_post( $source_post_id );

//    if ( !$original_post ) {
//       return new WP_Error( 'no_post', 'Post não encontrado', array( 'status' => 404 ) );
//    }

//    $postarr = array(
//       'post_title'   => $original_post->post_title,
//       'post_content' => $original_post->post_content,
//       'post_status'  => 'draft',
//       'post_author'  => get_current_user_id(),
//       // Adicione outros campos conforme necessário
//    );

//    $new_post_id = wp_insert_post( $postarr );

//    if ( is_wp_error( $new_post_id ) ) {
//       return $new_post_id;
//    }

//    return rest_ensure_response( array( 'new_post_id' => $new_post_id ) );
// 	error_log( 'Function clone_post_function just finished' );
// }

// // CREATE POST

// add_action( 'rest_api_init', function () {
// 	error_log( 'Action rest_api_init just started' );
//     register_rest_route( 'meuapp/v1', '/create-post/', array(
//         'methods' => 'POST',
//         'callback' => 'meuapp_create_post',
//         'permission_callback' => function () {
//             return current_user_can( 'edit_posts' );
//         }
//     ));
// 	error_log( 'Action rest_api_init just finished' );
// });

// function meuapp_create_post( $request ) {
// 	error_log( 'Function meuapp_create_post just started' );
//     $data = $request->get_json_params();

//     // Extracting data from the request
//     $title = sanitize_text_field( $data['title'] );
//     $address = sanitize_text_field( $data['address'] );
//     $rooms = sanitize_text_field( $data['rooms'] );
//     $tags = $data['tags']; // Assuming tags is an array of strings

//     // Fetch and prepare the template content
//     // Assuming you fetch the template content from somewhere and store it in $template_content
//     $post_content = $template_content;
//     $post_content = str_replace("{{address}}", $address, $post_content);
//     $post_content = str_replace("{{rooms}}", $rooms, $post_content);

//     // Create or fetch the category ID
//     $category_id = get_category_by_slug( $address );
//     if ( ! $category_id ) {
//         $category_id = wp_create_category( $address );
//     } else {
//         $category_id = $category_id->term_id;
//     }

//     // Create the post
//     $post_id = wp_insert_post([
//         'post_title'    => $title,
//         'post_content'  => $post_content,
//         'post_status'   => 'publish',
//         'post_author'   => get_current_user_id(),
//         'post_category' => array( $category_id ),
//         // Additional configurations...
//     ]);

//     // Check for insert post errors
//     if ( is_wp_error( $post_id ) ) {
//         return new WP_Error( 'post_creation_failed', 'Failed to create post', array( 'status' => 500 ) );
//     }

//     // Add tags to the post
//     wp_set_post_tags( $post_id, $tags );

//     return rest_ensure_response( array( 'message' => 'Post created successfully!', 'post_id' => $post_id ) );

// 	error_log( 'Function meuapp_create_post just finished' );
// }
