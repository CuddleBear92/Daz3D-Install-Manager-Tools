# Product Image Downloader
 Loads DAZ laucher metadata files and gathers the correspondent image from the product wiki.

# Dependencies:
`python 3`

`requests`

Install with: `pip -r requirement.txt`

# How to:
* Place the `product-image-downloader.py` script in `C:\Users\Public\Documents\DAZ 3D\InstallManager` (Default Location)
* Run the `product-image-downloader.py` script. (the script will download any images for any .dsx files in your download folder)
* The downloaded files will be saved in the `C:\Users\Public\Documents\DAZ 3D\InstallManager\Thumbnails` folder with the name corresponding product id.
* If any error occours it wil be logged on the `product-image-downloader.log`.

# Scrape image in ID range:
* Open the `product-image-downloader-id-range.py` and edit the start and end ID value numbers to set the range it will scrape from.
* Save the file and run it.
* The downloaded files will be saved in the `C:\Users\Public\Documents\DAZ 3D\InstallManager\Thumbnails` folder with the name corresponding product id.
* If any error occours it wil be logged on the `product-image-downloader-id-range.log`.


# [Product Image Cache](https://github.com/CuddleBear92/Daz3D-Install-Manager-Tools/tree/imagecache)
You can find a huge cache of the product images in the [image cache branch](https://github.com/CuddleBear92/Daz3D-Install-Manager-Tools/tree/imagecache).
