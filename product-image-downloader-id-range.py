import os
import re
import sys
import requests

# Configuration settings
START_PRODUCT_ID = 1
END_PRODUCT_ID = 120000
output_folder = 'C:\\Users\\Public\\Documents\\DAZ 3D\\InstallManager\\Thumbnails'
wiki_url = 'http://docs.daz3d.com/doku.php/public/read_me/index/', '/start'
image_reg = r'(https?:\/\/docs\.daz3d\.com\/lib\/exe\/fetch.php\?.+.jpg)" class="media" target'
log_name = "{0}{1}".format(os.path.basename(sys.argv[0])[:-3], '.log')
log_handler = open(log_name, 'a')

def save_to_log(text, error_type):
    global log_handler
    log = '[{0}] {1}'.format(error_type, text)
    try:
        print(log)
        log_handler.write('{0}\n'.format(log))
    except IOError:
        print('Error saving log\n Previous log: {0}\n'.format('[{0}] {1}'.format(error_type, text)))
        return

def save_jpg(data, product_id):
    # check if wiki page exists
    if re.search('Page Not Found', data.text):
        save_to_log('Product ID [{0}] Not Found'.format(product_id), 'WARN')
        return

    # find and filter image url
    try:
        result = re.sub(r'&amp;', '&', re.search(image_reg, data.text).group(1))
    except AttributeError:
        save_to_log('Product ID [{0}] - Image Doesn\'t exist'.format(product_id), 'NO_FILE')
        return

    try:
        # download image
        data = requests.get(result, allow_redirects=True)
    except Exception as e:  # CONNECTION ERROR
        save_to_log('Error downloading image: [{0}]'.format(e), 'CONNECTION_PHOTO')
        return
    else:
        try:
            # save image to file
            open('{0}/{1}.jpg'.format(output_folder, product_id), 'wb').write(data.content)
        except Exception as e:  # IO ERROR
            save_to_log('Error saving image: [{0}]'.format(e), 'FILE_IO')
            return

def get_wiki_page(product_id):
    try:
        # download wiki page
        data = requests.get('{0}{1}{2}'.format(wiki_url[0], product_id, wiki_url[1]), allow_redirects=True)
    except Exception as e:  # CONNECTION ERROR
        save_to_log('Error accessing wiki page for ID [{0}]: {1}'.format(product_id, e), 'CONNECTION_WIKI')
        return
    else:
        save_jpg(data, product_id)

def main():
    global log_handler

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # make output folder

    # Collect existing image files once at the start
    existing_files = set()
    for file in os.listdir(output_folder):
        if file.endswith('.jpg'):
            # Extract product ID from filename (remove .jpg extension)
            try:
                product_id = int(file[:-4])  # Remove '.jpg' and convert to int
                existing_files.add(product_id)
            except ValueError:
                continue  # Skip files that don't match the expected format

    # Loop through product IDs in the specified range
    for product_id in range(START_PRODUCT_ID, END_PRODUCT_ID + 1):
        # Check if file already exists using the set
        if product_id in existing_files:
            print(f"Product ID {product_id} - Image already exists")
            continue
        get_wiki_page(product_id)
    
    log_handler.close()

if __name__ == '__main__':
    main()
