If I am about to upload a entire project code for you, what is the most effient way of doing that, so you can help developing new functionalities?

Ok, here it goes:

Here are my project files: https://github.com/anfergainst/tmp_test_repo and I need you yo help me adding all new functionalities I need, ok?

First,
In the backend.py, I need you to make this api able to receive the url as a argument. So instead of specifying "url" in it's code, it dynamically get from who is calling. This should be a obrigatory field.
In the wordpress_realstate_api.py, I need you to make a iteraction the "urls" list from config.py and iterate with each address, passing them to the API



Create a block for each of those elements from my custom_api too (I called it wordpress_realstate_api):
- pt_text
- en_text
- images
- videos
- youtube_videos
- json_ld
- listing_details
- listing_details_brute
- features
- rooms
- energy_certificate
- energy_rating_info
- legal_disclaimer

Where:
- For pt_text and en_text I need a wordpress block that MAY appear when any of those are found and has a tab for "Português" (that may appear if found pt_text) and other for "English" (that may appear if found en_text)
- For images, I need you to get my Carrousel block from: wp_carrousel/*, where there has 3 files to make it work: wp_carrousel.css, wp_carrousel.html and wp_carrousel.js.
When using it, you must use all images URL's on block:
const images = [
  // List of image URLs
];
but remember to exclude the energyrating image (may vary urls, paths or filenames) that comes together. This image should not appear on carrousel.
- for videos, provide a simple block showing the video with 640x320 with playback functionalities if possible
- for youtube videos, provide a simple block for playing the video. Start always playing the video muted, with only play/stop and the bar to choose where from the video the user want to play.
- 
