import os
import argparse
import randomname

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



"""
A simple selenium test example written by python
"""        
class WaitLoad:
    def __call__(self, driver):
        response = driver.execute_script(
        """
            try {
                return window.player.time() == window.player.duration();
            } catch (e) {
                return e.message;
            }
        """
        )
        
        return response if type(response) == bool else False


def create_parser():
    arg_parser = argparse.ArgumentParser(description="*** Running end-user player")

    arg_parser.add_argument("--seed", type=int, default=0)
    arg_parser.add_argument("--video", type=int, default=1)
    arg_parser.add_argument("--abr", type=str, default="abrDynamic")
    arg_parser.add_argument("--user", type=str, default=randomname.get_name())
    arg_parser.add_argument("--bitratemax", type=int, default=30000)
    
    return arg_parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    seed = args.seed
    user = args.user
    abr = args.abr
    video = args.video

    os.makedirs(f'logs/{seed}/{user}', exist_ok = True)


    """Start web driver"""
    chrome_options =  webdriver.ChromeOptions()
    
    chrome_options.add_argument('--verbose')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless=new')
#    chrome_options.add_argument('--auto-open-devtools-for-tabs')
    # chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--disk-cache-dir=/dev/null')
    chrome_options.add_argument('--no-user-gesture-required')
    # chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(f'--user-data-dir=logs/{seed}/{user}')

    chrome_local_state_prefs = {
        "browser.enabled_labs_experiments": [
            "block-insecure-private-network-requests@2"
        ],
    }
    chrome_options.add_experimental_option("localState", chrome_local_state_prefs)
    
    driver = webdriver.Chrome(options=chrome_options)

    """Watching BBB Video Streaming"""
    driver.get(
        f'http://10.0.1.53:30001/player/vod-client-local-{video}.html?abr={abr}&uid={user}&btrmax={args.bitratemax}'
    )
 
    try:
        WebDriverWait(driver, 634).until(WaitLoad())
    except TimeoutException as e:
        print("Exception triggered", e)


    """Stop web driver"""
    driver.get_screenshot_as_file(f'logs/{seed}/{user}-screenshot.png')
        
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
