import requests
import json
from requests.auth import HTTPBasicAuth
import os

# Load environment variables
wordpress_url = os.environ.get('WORDPRESS_URL')
username = os.environ.get('WORDPRESS_USERNAME')
password = os.environ.get('WORDPRESS_PASSWORD')

### WP FUNC
# add_action( 'rest_api_init', function () {
#    register_rest_route( 'meuapp/v1', '/clone-post/', array(
#       'methods' => 'POST',
#       'callback' => 'clone_post_function',
#       'permission_callback' => function () {
#          return current_user_can( 'edit_posts' );
#       }
#    ));
# });

# function clone_post_function( $request ) {
#    $source_post_id = $request['source_post_id'];
#    $original_post = get_post( $source_post_id );

#    if ( !$original_post ) {
#       return new WP_Error( 'no_post', 'Post não encontrado', array( 'status' => 404 ) );
#    }

#    $postarr = array(
#       'post_title'   => $original_post->post_title,
#       'post_content' => $original_post->post_content,
#       'post_status'  => 'draft',
#       'post_author'  => get_current_user_id(),
#       // Adicione outros campos conforme necessário
#    );

#    $new_post_id = wp_insert_post( $postarr );

#    if ( is_wp_error( $new_post_id ) ) {
#       return $new_post_id;
#    }

#    return rest_ensure_response( array( 'new_post_id' => $new_post_id ) );
# }
##########
def clone_wordpress_post(source_post_id, wordpress_url, username, password):
    url = f"{wordpress_url}/wp-json/meuapp/v1/clone-post/"
    data = {'source_post_id': source_post_id}
    auth = HTTPBasicAuth(username, password)

    response = requests.post(url, json=data, auth=auth)

    if response.status_code != 200:
        return f"Erro: {response.text}"

    return response.json()

# Exemplo de Uso
source_post_id = 1046  # Substitua pelo ID do post que deseja clonar
result = clone_wordpress_post(source_post_id, wordpress_url, username, password)
print(result)