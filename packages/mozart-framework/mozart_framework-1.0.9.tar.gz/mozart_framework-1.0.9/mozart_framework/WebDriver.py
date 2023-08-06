#=============================================================
#=================     Library Import    =====================
#=============================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Biblioteca usada para movimentos de mouse e Hover
from selenium.webdriver.common.action_chains import ActionChains
# Biblioteca usada para comandos de ComboBox
from selenium.webdriver.support.select import Select

import time
import sys
import os
from pathlib import Path
import chromedriver_autoinstaller
import geckodriver_autoinstaller

from mozart_framework.LogDriver import LogAutomator

import logging
from geckodriver_autoinstaller import utils
import urllib
import urllib.request
import urllib.error

from io import BytesIO

import zipfile

#=============================================================
#=================        class          =====================
#=============================================================

# Classe BrowserAutomator Resposável pela automatização do processo usando a interface WEB
class BrowserAutomator:

    # Browser
    browser = webdriver.Firefox

    logger = LogAutomator()

    actualDirectory = ""

    def __init__(self):
        if getattr(sys, 'frozen', False):
            # frozen
            self.actualDirectory = Path(os.path.dirname(sys.executable)).parent
        else:
            # unfrozen
            self.actualDirectory =  Path(os.path.dirname(os.path.realpath(__file__))).parent

    def get_geckodriver_url(self, version):
        """
        Generates the download URL for current platform , architecture and the given version.
        Supports Linux, MacOS and Windows.
        :param version: the version of geckodriver
        :return: Download URL for geckodriver
        """
        platform, architecture = utils.get_platform_architecture()
        return f'https://github.com/mozilla/geckodriver/releases/download/{version}' \
               f'/geckodriver-{version}-{platform}{architecture}.zip'


    def downloadGeckodriver(self , cwd=False):
        """
            Appends the directory of the geckodriver binary file to PATH.

            :param cwd: Flag indicating whether to download to current working directory
            :return: The file path of geckodriver
            """
        #geckodriver_filepath = utils.download_geckodriver(cwd)

        firefox_version = utils.get_firefox_version()
        if not firefox_version:
            logging.debug('Firefox is not installed.')
            return
        geckodriver_version = utils.get_latest_geckodriver_version()
        if not geckodriver_version:
            logging.debug('Can not find latest version of geckodriver.')
            return

        if cwd:
            geckodriver_dir = os.path.join(
                os.path.abspath(os.getcwd()),
                geckodriver_version
            )
        else:
            geckodriver_dir = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                geckodriver_version
            )
        geckodriver_filename = utils.get_geckodriver_filename()
        geckodriver_filepath = os.path.join(geckodriver_dir, geckodriver_filename)
        if not os.path.isfile(geckodriver_filepath):
            logging.debug(f'Downloading geckodriver ({geckodriver_version})...')
            if not os.path.isdir(geckodriver_dir):
                os.mkdir(geckodriver_dir)
            url = self.get_geckodriver_url(geckodriver_version)
            try:
                response = urllib.request.urlopen(url)
                if response.getcode() != 200:
                    raise urllib.error.URLError('Not Found')
            except urllib.error.URLError:
                raise RuntimeError(f'Failed to download geckodriver archive: {url}')
            archive = BytesIO(response.read())
            with zipfile.ZipFile(archive) as zip_file:
                zip_file.extract(geckodriver_filename, geckodriver_dir)
        else:
            logging.debug('geckodriver is already installed.')
        if not os.access(geckodriver_filepath, os.X_OK):
            os.chmod(geckodriver_filepath, 0o744)

        if not geckodriver_filepath:
            logging.debug('Can not download geckodriver.')
            return
        geckodriver_dir = os.path.dirname(geckodriver_filepath)
        if 'PATH' not in os.environ:
            os.environ['PATH'] = geckodriver_dir
        elif geckodriver_dir not in os.environ['PATH']:
            os.environ['PATH'] = geckodriver_dir + utils.get_variable_separator() + os.environ['PATH']
        return geckodriver_filepath

    # Função que abre o Firefox com uma URL passada por parâmetro
    def openFirefox(self,URL, downloadPath = ""):


        options = webdriver.FirefoxProfile()
        options.set_preference("browser.preferences.instantApply" , True)
        options.set_preference("browser.download.folderList", 2)
        if downloadPath != "" :
            options.set_preference("browser.download.dir", downloadPath)
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/excel,application/octet-stream")
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.manager.showAlertOnComplete", False)
        options.set_preference("browser.helperApps.alwaysAsk.force", False)

        #geckodriver = geckodriver_autoinstaller.install()
        geckodriver = self.downloadGeckodriver()

        self.browser=webdriver.Firefox(firefox_profile=options,executable_path=r''+ geckodriver +'')
        if URL != "" :
            self.browser.get(URL)
            self.logger.writeLog("INFO", "Firefox Browser Opened Successfully with URL:" + URL)

    def navigateTo(self,URL):
        self.browser.get(URL)

        self.logger.writeLog("INFO", "Browser Opened Successfully with URL:" + URL)

    # Função que abre o Chrome com uma URL passada por parâmetro
    def openChrome(self,URL):

        chromedriver = chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        self.browser = webdriver.Chrome(executable_path=r'' + chromedriver + '', chrome_options=chrome_options)
        if URL != "":
            self.browser.get(URL)
            self.logger.writeLog("INFO", "Chrome Browser Opened Successfully with URL:" + URL)

    # Função que abre o IE com uma URL passada por parâmetro
    def openIE(self,URL, iedriverpath):

        options = webdriver.IeOptions()

        caps = DesiredCapabilities.INTERNETEXPLORER
        caps['ignoreProtectedModeSettings'] = True
        caps['initialBrowserUrl'] = "http://www.google.com.br"

        options.set_capability('InternetExplorerDriver.NATIVE_EVENTS', False)
        self.browser=webdriver.Ie(options=options,executable_path=r'' + iedriverpath + '',capabilities=caps)
        if URL != "" :
            self.browser.get(URL)
            self.logger.writeLog("INFO", "IE Browser Opened Successfully with URL:" + URL)

    def waitElementInvisibility(self,findType,lookProperty,maxdelay=20):
        if findType == 'XPATH':
            WebDriverWait(self.browser, maxdelay).until(EC.invisibility_of_element((By.XPATH,lookProperty)))
        if findType == 'CSS_SELECTOR':
            element = WebDriverWait(self.browser, maxdelay).until(
                EC.invisibility_of_element((By.CSS_SELECTOR, lookProperty)))
        if findType == 'CLASS_NAME':
            element = WebDriverWait(self.browser, maxdelay).until(
                EC.invisibility_of_element((By.CLASS_NAME, lookProperty)))
            #print("invisivel")

    def waitElementBeDisplayed(self,findType,lookProperty,maxdelay=20):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = self.browser.find_element_by_xpath(lookProperty)
        if findType == 'CSS_SELECTOR':
            element = self.browser.find_element_by_css_selector(lookProperty)

        i = 0
        while element.is_displayed() == False and i < maxdelay:
            time.sleep(1)
            i = i+1

        return element.is_displayed()


    def waitElementNotBeDisplayed(self,findType,lookProperty,maxdelay=20):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = self.browser.find_element_by_xpath(lookProperty)
        if findType == 'CSS_SELECTOR':
            element = self.browser.find_element_by_css_selector(lookProperty)

        i = 0
        while element.is_displayed() == True and i < maxdelay:
            time.sleep(1)
            i = i+1

    def getXpathByName(self, texto,maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        element = self.browser.find_element_by_xpath("//*[contains(text(), '" + texto + "')]")
        xpath = self.browser.browser.execute_script("function absoluteXPath(element) {" +
                                               "var comp, comps = [];" +
                                               "var parent = null;" +
                                               "var xpath = '';" +
                                               "var getPos = function(element) {" +
                                               "var position = 1, curNode;" +
                                               "if (element.nodeType == Node.ATTRIBUTE_NODE) {" +
                                               "return null;" +
                                               "}" +
                                               "for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling) {" +
                                               "if (curNode.nodeName == element.nodeName) {" +
                                               "++position;" +
                                               "}" +
                                               "}" +
                                               "return position;" +
                                               "};" +

                                               "if (element instanceof Document) {" +
                                               "return '/';" +
                                               "}" +

                                               "for (; element && !(element instanceof Document); element = element.nodeType == Node.ATTRIBUTE_NODE ? element.ownerElement : element.parentNode) {" +
                                               "comp = comps[comps.length] = {};" +
                                               "switch (element.nodeType) {" +
                                               "case Node.TEXT_NODE:" +
                                               "comp.name = 'text()';" +
                                               "break;" +
                                               "case Node.ATTRIBUTE_NODE:" +
                                               "comp.name = '@' + element.nodeName;" +
                                               "break;" +
                                               "case Node.PROCESSING_INSTRUCTION_NODE:" +
                                               "comp.name = 'processing-instruction()';" +
                                               "break;" +
                                               "case Node.COMMENT_NODE:" +
                                               "comp.name = 'comment()';" +
                                               "break;" +
                                               "case Node.ELEMENT_NODE:" +
                                               "comp.name = element.nodeName;" +
                                               "break;" +
                                               "}" +
                                               "comp.position = getPos(element);" +
                                               "}" +

                                               "for (var i = comps.length - 1; i >= 0; i--) {" +
                                               "comp = comps[i];" +
                                               "xpath += '/' + comp.name.toLowerCase();" +
                                               "if (comp.position !== null) {" +
                                               "xpath += '[' + comp.position + ']';" +
                                               "}" +
                                               "}" +

                                               "return xpath;" +

                                               "} return absoluteXPath(arguments[0]);", element)

        return xpath

    # Função que Clica no elemento em uma página, fintType é qual o tipo de busca que será feito na página, lookproperty é o parâmetro de busca que será usado, e o maxdelay é o tempo máximo que o bot vai esperar para que o objeto exista
    def clickElement(self,findType,lookProperty, maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, lookProperty)))
            #element = self.browser.find_element_by_xpath(lookProperty)
        if findType == 'CSS_SELECTOR':
            element = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, lookProperty)))
            #element = self.browser.find_element_by_css_selector(lookProperty)
        element.click()
        self.logger.writeLog("INFO", "Element: " + lookProperty +" clicked with success.")

        # Função que Clica no elemento em uma página, fintType é qual o tipo de busca que será feito na página, lookproperty é o parâmetro de busca que será usado, e o maxdelay é o tempo máximo que o bot vai esperar para que o objeto exista

    def hoverElement(self, findType, lookProperty, maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, lookProperty)))
            # element = self.browser.find_element_by_xpath(lookProperty)
        if findType == 'CSS_SELECTOR':
            element = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, lookProperty)))
            # element = self.browser.find_element_by_css_selector(lookProperty)
        action = ActionChains(self.browser)
        action.move_to_element(element).perform()
        self.logger.writeLog("INFO", "Element: " + lookProperty + " hovered with success.")

    def moveToElement(self, findType, lookProperty, maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = self.browser.find_element_by_xpath(lookProperty)

        if findType == 'CSS_SELECTOR':
            element = self.browser.find_element_by_css_selector(lookProperty)
        element.location_once_scrolled_into_view
        self.logger.writeLog("INFO", "Element: " + lookProperty + " scrolled with success.")

    # Função que digita no elemento em uma página, textToType será o texto digitado, fintType é qual o tipo de busca que será feito na página, lookproperty é o parâmetro de busca que será usado, e o maxdelay é o tempo máximo que o bot vai esperar para que o objeto exista
    def typeElement(self,findType,lookProperty, textToType, clear=True, maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = self.browser.find_element_by_xpath(lookProperty)
        if findType == 'CSS_SELECTOR':
            element = self.browser.find_element_by_css_selector(lookProperty)
        if clear == True :
            element.clear()
        element.send_keys(textToType)
        self.logger.writeLog(r"INFO", r"Element: " + lookProperty +" typed text.")

    def getValue(self, findType, lookProperty, maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = self.browser.find_element_by_xpath(lookProperty)
        if findType == 'CSS_SELECTOR':
            element = self.browser.find_element_by_css_selector(lookProperty)
        self.logger.writeLog("INFO", "Element: " + lookProperty + " returned text " + element.text + ".")
        return element.get_attribute("value")

    # Função que retorna o texto de um elemento na página, fintType é qual o tipo de busca que será feito na página, lookproperty é o parâmetro de busca que será usado, e o maxdelay é o tempo máximo que o bot vai esperar para que o objeto exista
    def getElementInnerText(self,findType,lookProperty, maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = self.browser.find_element_by_xpath(lookProperty)
        if findType == 'CSS_SELECTOR':
            element = self.browser.find_element_by_css_selector(lookProperty)
        self.logger.writeLog("INFO", "Element: " + lookProperty +" returned text " + element.text + ".")
        return element.text

    # Função que seleciona um elemento do combobox pelo texto em uma página, textToSelect será o texto a ser selecionado, findType é qual o tipo de busca que será feito na página, lookproperty é o parâmetro de busca que será usado, e o maxdelay é o tempo máximo que o bot vai esperar para que o objeto exista
    def selectItemByTextOnComboBox(self,findType,lookProperty, textToSelect , maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = Select(self.browser.find_element_by_xpath(lookProperty))
        if findType == 'CSS_SELECTOR':
            element = Select(self.browser.find_element_by_css_selector(lookProperty))
        element.select_by_visible_text(textToSelect)
        self.logger.writeLog("INFO", "Element: " + lookProperty +" selected item " + textToSelect + " on ComboBox.")

    # Função que seleciona um elemento do combobox pelo o indice em uma página, indexToSelect será o indice a ser selecionado, findType é qual o tipo de busca que será feito na página, lookproperty é o parâmetro de busca que será usado, e o maxdelay é o tempo máximo que o bot vai esperar para que o objeto exista
    def selectItemByIndexOnComboBox(self,findType,lookProperty, indexToSelect , maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = Select(self.browser.find_element_by_xpath(lookProperty))
        if findType == 'CSS_SELECTOR':
            element = Select(self.browser.find_element_by_css_selector(lookProperty))
        element.select_by_index(indexToSelect)
        self.logger.writeLog("INFO", "Element: " + lookProperty +" selected item by index: " + indexToSelect + " on ComboBox.")


    def selectItemByValue(self, findType, lookProperty , value, maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = Select(self.browser.find_element_by_xpath(lookProperty))
        if findType == 'CSS_SELECTOR':
            element = Select(self.browser.find_element_by_css_selector(lookProperty))
        element.select_by_value(value)
        self.logger.writeLog("INFO",
                             "Element: " + lookProperty + " selected value " + value + ".")

    # Função que retorna o texto do elemento selecionado no combobox na página, fintType é qual o tipo de busca que será feito na página, lookproperty é o parâmetro de busca que será usado, e o maxdelay é o tempo máximo que o bot vai esperar para que o objeto exista
    def getSelectedItemTextOnComboBox(self,findType,lookProperty, maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            element = Select(self.browser.find_element_by_xpath(lookProperty))
        if findType == 'CSS_SELECTOR':
            element = Select(self.browser.find_element_by_css_selector(lookProperty))
        self.logger.writeLog("INFO", "Element: " + lookProperty +" returned text " + element.first_selected_option.text + ".")
        return element.first_selected_option.text

    def checkElementExists(self,findType, lookProperty, maxdelay = 4):
        try:
            self.browser.implicitly_wait(maxdelay)
            if findType == 'XPATH':
                element = self.browser.find_element_by_xpath(lookProperty)
            if findType == 'CSS_SELECTOR':
                element = self.browser.find_element_by_css_selector(lookProperty)
            self.logger.writeLog("INFO", "Element: " + lookProperty + " found in page")
            return True
        except:
            self.logger.writeLog("INFO", "Element: " + lookProperty + " NOT found in page")
            return False

    def switchToFrame(self,findType,lookProperty, maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        if findType == 'XPATH':
            frame = self.browser.find_element_by_xpath(lookProperty)
        if findType == 'CSS_SELECTOR':
            frame = self.browser.find_element_by_css_selector(lookProperty)
        self.browser.switch_to.frame(frame)
        self.logger.writeLog("INFO", "Frame: " + lookProperty +" switched to context.")

    def switchtoMainWindow(self):
        self.browser.switch_to.default_content()
        self.logger.writeLog("INFO", "Selenium is back to the Main Window.")

    # Função que extrai uma tabela em uma ARRAY de acordo com o XPATH

    # O lookPropertyROW, representa a primeira linha da primeira coluna, porém deve se esconder a número da linha EX: "/html/body/div[6]/div[1]/div[1]/div[3]/div/table/tbody/tr/td[1]". No fim, a tag tr está sem número
    # O lookProperyColumn, representa a primeira linha (excluindo o cabecalho), porém deve se esconder o número da coluna EX: "/html/body/div[6]/div[1]/div[1]/div[3]/div/table/tbody/tr[2]/td". No fim, a  tag td está sem número e a tr está apontando para a primeira linha(excluindo o cabeçalho)
    # O lookPropertyCell, representa o XPATH da celula, porém deverá ser editado para conter a seguinte informação, rowID e columnID. Ex: "/html/body/div[6]/div[1]/div[1]/div[3]/div/table/tbody/tr[rowID]/td[columnID]". No fim, rowID e columnID deverá ser as referências da celula.
    def extractTableToArrayByXPATH(self,findType,lookPropertyRow,lookPropertyColumn, lookPropertyCell, maxdelay=15):
        self.browser.implicitly_wait(maxdelay)
        row = self.browser.find_elements_by_xpath(lookPropertyRow)

        column = self.browser.find_elements_by_xpath(lookPropertyColumn)

        i = 1
        matriz = []
        if len(column) > 0:
            while (i <= len(row) + 1):
                aux = []
                j = 1
                while (j <= len(column)):
                    cell = lookPropertyCell.replace("rowID", str(i))
                    cell = cell.replace("columnID", str(j))
                    try:
                        node = self.browser.find_element_by_xpath(cell)
                        aux.append(node.text.lstrip().rstrip())
                    except:
                        aux.append("")
                    j = j + 1
                i = i + 1
                matriz.append(aux)
        return matriz
