# Product Image Downloader
 Loads DAZ laucher metadata files and gathers the correspondent image from the product wiki.

# Dependencies:
`python 3`

`requests`

Install with: `pip -r requeriments.txt`

# How to:
* Place the metadata files in the `dsx_files` folder.
* Run the `product-image-downloader.py` script.
* The downloaded files will be saved in the `image cache` folder with the name corresponding product id.
* If any error occours it wil be logged on the `product-image-downloader.log`.
* If 3 or more errors occurs back to back the program will be terminated.
