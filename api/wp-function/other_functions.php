
add_action( 'rest_api_init', function () {
    register_rest_route( 'devops/v1', '/create-from-template/', array(
        'methods' => 'POST',
        'callback' => 'create_from_template',
//         'permission_callback' => function () {
//             return current_user_can( 'edit_posts' );
//         }
	) );
} );







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
