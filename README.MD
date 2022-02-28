# Product Image Downloader
 Loads DAZ laucher metadata files and gathers the correspondent image from the product wiki.

# Dependencies:
`python 3`

`requests`

Install with: `pip -r requeriments.txt`

# How to:
* Place the metadata files in the `dsx_files` folder. (You can also edit this to your Daz Installer Manager Download directory.)
* Run the `product-image-downloader.py` script.
* The downloaded files will be saved in the `C:\Users\Public\Documents\DAZ 3D\InstallManager\Thumbnails` folder with the name corresponding product id.
* If any error occours it wil be logged on the `product-image-downloader.log`.


# [Product Image Cache](https://github.com/CuddleBear92/Daz3D-Install-Manager-Tools/tree/imagecache)
You can find a huge cache of the product images in the [image cache branch](https://github.com/CuddleBear92/Daz3D-Install-Manager-Tools/tree/imagecache).
