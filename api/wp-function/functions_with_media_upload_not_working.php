/**
 * DevOps.click CUSTOM API for WordPress.
 * Clone/Update Real State Posts
 */

add_action( 'rest_api_init', function () {
    register_rest_route( 'devops/v1', '/create-from-template/', array(
        'methods' => 'POST',
        'callback' => 'create_from_template',
	) );
} );

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

function download_and_set_featured_image($image_url, $post_id) {
    global $wpdb;

    if (empty($image_url)) {
        return false; // Return false if the URL is empty
    }

    // Check if the image already exists in the media library
    $query = "SELECT ID FROM {$wpdb->posts} WHERE post_type='attachment' AND guid='%s'";
    $attachment_id = $wpdb->get_var($wpdb->prepare($query, $image_url));

    if ($attachment_id) {
        // Image already exists, set it as the featured image
        set_post_thumbnail($post_id, $attachment_id);
        return true;
    }

    // Image does not exist, download and upload it
    $tmp = download_url($image_url);

    // Check for download errors
    if (is_wp_error($tmp)) {
        return false;
    }

    $file_array = array(
        'name' => basename($image_url),
        'tmp_name' => $tmp,
    );

    // Upload the image file to the WordPress Media Library
    $id = media_handle_sideload($file_array, $post_id);

    // Check for sideload errors
    if (is_wp_error($id)) {
        @unlink($file_array['tmp_name']); // Clean up any temp file
        return false;
    }

    // Set the uploaded image as the featured image
    set_post_thumbnail($post_id, $id);

    return true;
}

function update_featured_image_if_changed($new_image_url, $post_id) {
    if (empty($new_image_url)) {
        return false; // Return false if the new URL is empty
    }

    // Get the current featured image ID
    $current_featured_image_id = get_post_thumbnail_id($post_id);

    // If there is no current featured image, simply set the new one
    if (!$current_featured_image_id) {
        return download_and_set_featured_image($new_image_url, $post_id);
    }

    // Get the URL of the current featured image
    $current_featured_image_url = wp_get_attachment_url($current_featured_image_id);

    // Check if the current image URL matches the new URL
    if ($current_featured_image_url === $new_image_url) {
        return true; // The image is the same, no update needed
    }

    // The URLs are different, so update the featured image
    return download_and_set_featured_image($new_image_url, $post_id);
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

    // For featured media
    $featured_media_id = get_media_id_from_url($post_data['featured_image']);

    // Prepare new post data
    $new_post_data = array(
        'post_title'    => $post_data['title'],
        'post_content'  => $content,
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
            'post_content' => $content, // Updated content from template
            // Add other fields you want to update here
        );

        // Update the post
        $updated_post_id = wp_update_post( $updated_post_data );

        // Update the meta fields
        foreach ($template_meta as $key => $values) {
            foreach ($values as $value) {
                update_post_meta( $existing_post_id, $key, $value );
            }
        }

        // Update the spectra custom meta fields for the updated post
        update_post_meta($existing_post_id, 'spectra_custom_meta', $template_spectra_custom_meta);

        // Update featured image if the URL has changed
        update_featured_image_if_changed($post_data['featured_image'], $existing_post_id);

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

        // Update the spectra custom meta fields for the new post
       update_post_meta($new_post_id, 'spectra_custom_meta', $template_spectra_custom_meta);

       // Download and set featured image
       download_and_set_featured_image($post_data['featured_image'], $new_post_id);
    }
}
