add_action( 'rest_api_init', function () {
    register_rest_route( 'devops/v1', '/create-from-template/', array(
        'methods' => 'POST',
        'callback' => 'create_from_template',
//         'permission_callback' => function () {
//             return current_user_can( 'edit_posts' );
//         }
	) );
} );

function create_from_template( $request ) {
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
        'post_title'    => $post_data['title'],
        'post_content'  => $content,
        'post_excerpt'  => $template_post->post_excerpt,
        'post_author'   => $template_post->post_author,
        // More fields here...
        'post_status'   => 'publish',
    );

    // Insert the new post
    $new_post_id = wp_insert_post( $new_post_data );

    if ( $new_post_id === 0 ) {
        return new WP_Error( 'post_creation_failed', 'Failed to create post', array( 'status' => 500 ) );
    }

    // Return success message and new post ID
    return array( 'message' => 'Post created successfully!', 'post_id' => $new_post_id );
}