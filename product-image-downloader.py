import os, re, sys, requests

dsx_files = 'dsx_files'
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

def save_jpg(data, product_id, metadata_file_name):

    # check if wiki page exists
    if re.search('Page Not Found', data.text):
        save_to_log('Product ID [{0}] Not Found - DSX file [{1}]'.format(product_id, metadata_file_name), 'WARN')
        return

    # find and filter image url
    try:
        result = re.sub(r'&amp;', '&', re.search(image_reg, data.text).group(1))
    except AttributeError:
        try:
            result = re.search(image_reg, data.text)
        except AttributeError:
            save_to_log('Product ID [{0}] - Image Doesn\'t exists [{1}]'.format(product_id, metadata_file_name), 'NO_FILE')
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


def get_wiki_page(product_id, metadata_file_name):
    try:
        # download wiki page
        data = requests.get('{0}{1}{2}'.format(wiki_url[0], product_id, wiki_url[1]), allow_redirects=True)
    except Exception as e:  # CONNECTION ERROR
        save_to_log('Error saving file [{0}]'.format(e), 'CONNECTION_WIKI')
        return
    else:
        save_jpg(data, product_id, metadata_file_name[:-4])


def main():
    global log_handler

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)  # make output folder

    if not os.path.exists(dsx_files):
        os.mkdir(dsx_files)  # make dsx folder

    # loop thought dsx files
    for (root, dirs, files) in os.walk(dsx_files):
        for file in files:
            text = ''

            # get product ID
            try:
                product_id = re.findall(r'IM0+([0-9]+)-', file)[0]
            except AttributeError:
                save_to_log('Could not find ID on file {0}'.format(file), 'WARN')
                continue
            else:
                text += product_id
                # check if file already exists
                if os.path.isfile('{0}/{1}.jpg'.format(output_folder, product_id)):
                    text += ' - [{0}]'.format(file[:-4])  # file already exists
                    print(text)
                    continue

                get_wiki_page(product_id, file)
    log_handler.close()

if __name__ == '__main__':
    main()
