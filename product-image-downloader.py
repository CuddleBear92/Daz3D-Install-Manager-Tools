import os, re, sys, requests
import xml.etree.ElementTree as eT

consecutive_errors = 0
dsx_files = 'dsx_files'
output_folder = 'image cache'
wiki_url = 'http://docs.daz3d.com/doku.php/public/read_me/index/', '/start'
image_reg = r'"(https?:\/\/docs\.daz3d\.com\/lib\/exe\/fetch.php\?.+.jpg)" class="media" target'
log_name = "{0}{1}".format(os.path.basename(sys.argv[0])[:-3], '.log')
log_handler = open(log_name, 'a')

def save_to_log(text, error_type):
    global consecutive_errors, log_handler
    log = 'ERRN[{0}][{1}] {2}'.format(consecutive_errors, error_type, text)
    try:
        print(log)
        log_handler.write(log)
    except IOError:
        consecutive_errors += 1
        print('Error saving log\n Previous log: {0}\n'.format('[{0}] {1}'.format(error_type, text)))
        return

def save_jpg(data, product_id):
    global consecutive_errors
    # print('{0}{1}{2}'.format(wiki_url[0], product_id, wiki_url[1]))

    # find and filter image url
    if re.search('Page Not Found', data.text):
        save_to_log('Product ID [{0}] Not Found'.format(product_id), 'WARN')
        return

    result = re.sub(r'&amp;', '&', re.search(image_reg, data.text).group(1))

    try:
        # download image
        data = requests.get(result, allow_redirects=True)
    except Exception as e:  # CONNECTION ERROR
        consecutive_errors += 1
        save_to_log('Error downloading image: [{0}]'.format(e), 'CONNECTION PHOTO')
        return
    else:
        try:
            # save image to file
            open('{0}/{1}.jpg'.format(output_folder, product_id), 'wb').write(data.content)
        except Exception as e:  # IO ERROR
            consecutive_errors += 1
            save_to_log('Error saving image: [{0}]'.format(e), 'FILEIO')
        else:
            consecutive_errors = 0


def get_wiki_page(product_id):
    global consecutive_errors

    try:
        # download wiki page
        data = requests.get('{0}{1}{2}'.format(wiki_url[0], product_id, wiki_url[1]), allow_redirects=True)
    except Exception as e:  # CONNECTION ERROR
        save_to_log('Error saving file [{0}]'.format(e), 'CONNECTION WIKI')
        consecutive_errors += 1
        return
    else:
        save_jpg(data, product_id)


def main():
    global consecutive_errors, log_handler
    text = ''
    
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)  # make output folder

    if not os.path.exists(dsx_files):
        os.mkdir(dsx_files)  # make dsx folder

    # loop thought dsx files
    for (root, dirs, files) in os.walk(dsx_files):
        for file in files:
            text = ''
            if consecutive_errors >= 3:
                save_to_log('Too many consecutive errors exiting', 'FATAL')
                log_handler.close()
                exit(-1)

            # parses XML file
            dsx_root = eT.parse('{0}/{1}'.format(dsx_files, file)).getroot()
            # get product ID
            try:
                product_id = re.findall(r'[0-9]+', dsx_root.findall('ProductStoreIDX')[0].attrib['VALUE'])[0]
            except AttributeError:
                save_to_log('Could not find ID on file {0}'.format(file), 'WARN')
                continue
            else:
                text += product_id
                # check if file already exists
                if os.path.isfile('{0}/{1}.jpg'.format(output_folder, product_id)):
                    text += ' .'  # file already exists
                    print(text)
                    continue

                get_wiki_page(product_id)
    log_handler.close()

if __name__ == '__main__':
    main()
