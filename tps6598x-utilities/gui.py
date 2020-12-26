import sys
import os
import cherrypy
from device_rw import *
import hw_interface
import register_class
from hi_functions import *
import webbrowser
import simplejson
import config
import time
import traceback

#### Globals ####

connected = None
handle = hw_interface(config.DEVICE_I2C_ADDR, config.HW_INTERFACE)

file_path = os.getcwd().replace("\\", "/")
#file_path = os.getcwd()

rp0 = 0x0000
rp1 = 0x0000
rp_select = 0
region_file = None
region_pointer = 0x0

filedata = bytearray()
spifiledata = bytearray()
numBlocks = -1
numSpiBlocks = -1
flashAbort = 0
spiFlashAbort = 0

i2cvariables = { 'sector' : 0, 'numBlocks': 0, 'count' : 0, 'error_msg' : "Unknown Error Encountered."}
spivariables = { 'sector' : 0, 'addr': 0, 'posn' : 0, 'length' : 0, 'count' : 0, 'compval' : True, 'error_msg' : "Unknown Error Encountered." }

def escape_html(instring) :
    replaceTable = {'<' : '&lt;',
                    '>' : '&gt;',
                    }

    outstring = str(instring)
    for replaceMap in replaceTable :
        outstring = outstring.replace(replaceMap, replaceTable[replaceMap])

    return outstring

#################            
def makeSelect(translate_list, register, index, value, parent_type, parent_name):
    retString = ""
    retString += """<select value=%d onchange="jsOnChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> \n""" %(value, register, index, parent_type, parent_name)
    i = 0
    for item in translate_list:
        if (value == i):
            retString += '    <option value=%d selected="selected">%s</option> \n' %(i, item)
        else:
            retString += '    <option value=%d>%s</option> \n' %(i, item)
        i += 1
    retString += '</select> \n'

    return retString

def makeFuncSelect(translate_list, function, index, value, parent_type, parent_name):
    retString = ""
    retString += """<select value=%d onchange="jsFuncChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> \n""" %(value, function, index, parent_type, parent_name)
    i = 0
    for item in translate_list:
        if (value == i):
            retString += '    <option value=%d selected="selected">%s</option> \n' %(i, item)
        else:
            retString += '    <option value=%d>%s</option> \n' %(i, item)
        i += 1
    retString += '</select> \n'

    return retString

def translateRegPtr(value):
    return '0x%x' %value

def revTranslateRegPtr(value):
    if value < 0x2000:
        value = 0x2000
    return '0x%x' %value

def convtohtml(retval) :
    retString = ""
    for char in str(retval) :
        if (char == "\n"):
            retString = retString + "<br>"
        else:
            retString = retString + char
            
    return retString

def processExecWrapper(execFunc, myFunction, handle, retval) :
    retval = execFunc(myFunction, handle)


class StringGenerator(object):
    @cherrypy.expose
    def exitguipage(self):
        retString = "<html><body>"

        retString += "<h1> TPS6598x Host Interface Tools are exiting </h1>"
        retString += "</html></body>"

        return retString

    @cherrypy.expose
    def exitgui(self):
        cherrypy.engine.exit()

    @cherrypy.expose
    def index(self):

        with open("html/index.html", "r") as myfile:
            retString = myfile.read()

        return retString

    @cherrypy.expose
    def report_connect(self):
        global connected

        if connected == True:
            retString = """<div style="display:inline;color:#ffffff;">Hardware CONNECTED</div>"""
        elif connected == False:
            retString = """<div style="display:inline;color:#ffffff;">Hardware DISCONNECTED</div>"""
        else:
            retString = """Hardware Connection UNTESTED"""

        return retString

    @cherrypy.expose
    def test_connect(self):
        global connected
        global handle
        global config

        try:
            handle.hw_close()
            handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                           config.DEVICE_I2C_ADDR)
            MODE_REG.read(handle)
            handle.hw_close()
            connected = True
            retString = """<div style="display:inline;color:#ffffff;">Hardware CONNECTED</div>"""
            return retString

        except Exception as myExc:
            e = sys.exc_info()
            handle.hw_close()
            print 'failed interface init on startup:\n'
            print '%s\n%s\n%s' % (e[0], traceback.print_exc(e[2]), myExc.message)
            handle.hw_close()
            connected = False
            retString = """<div style="display:inline;color:#ffffff;">Hardware DISCONNECTED</div>"""
            return retString

    @cherrypy.expose
    def iic_scanner_warning(self):
        retString = "<h1>I2C Addresses Scanner</h1>"

        retString += "<p>Beginning Scan...</p>"
        retString += "<p>(This may take a while to complete)</p>"

        return retString

    @cherrypy.expose
    def iic_scanner(self):
        global connected
        global handle
        global config

        try:
            retString = "<h1>I2C Addresses Scanner</h1>"

            handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                           config.DEVICE_I2C_ADDR)

            retString += "<h2>Read from the following I2C Addresses:</h2>"
            foundOne = False
            tmpAddr = config.DEVICE_I2C_ADDR

            read_success = True

            for myAddr in range(0x7f):
                handle.hw_set_i2c_addr(myAddr)

                read_success = True
                try:
                    MODE_REG.read(handle)
                    foundOne = True
                except:
                    read_success = False

                if read_success == True:
                    retString += """<p style="padding-left: 100px">0x%x</p>""" % myAddr

            handle.hw_close()

            config.DEVICE_I2C_ADDR = tmpAddr
            handle.hw_set_i2c_addr(tmpAddr)

            if foundOne == False:
                retString += """<p style="padding-left: 100px">(none)</p>"""
                connected = False
            else:
                connected = True

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            handle.hw_close()
            retString += """<h1>Exception Encountered during I2C Address Scan</h1><p>%s<p>""" % e
            retString += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            connected = False
            return retString

    @cherrypy.expose
    def dismiss_warning(self):
        global config
        cherrypy.response.headers['Content-Type'] = 'application/json'
        returnDict = {'failure': 0, 'failure_message': 'No failure'}

        config.WARNING = 0
        return simplejson.dumps(returnDict)

    @cherrypy.expose
    def eliminate_warning(self):
        import config as localconfig
        cherrypy.response.headers['Content-Type'] = 'application/json'
        returnDict = {'failure': 0, 'failure_message': 'No failure'}

        config.WARNING = 0

        confString = ""
        with open("html\config_template.py", "r") as myfile:
            confString = myfile.read()
        confString = confString.replace('**HW_INT**', str(localconfig.HW_INTERFACE))
        confString = confString.replace('**IIC_ADDR**', '0x%x' % localconfig.DEVICE_I2C_ADDR)
        confString = confString.replace('**BR**', str(localconfig.BITRATE))
        confString = confString.replace('**SBR**', str(localconfig.SPIBITRATE))
        confString = confString.replace('**PRT**', str(localconfig.PORT))
        confString = confString.replace('**SPIPRT**', str(localconfig.SPI_PORT))
        confString = confString.replace('**WRNG**', str(config.WARNING))
        with open("config.py", "w") as myfile2:
            myfile2.write(confString)

        return simplejson.dumps(returnDict)

    @cherrypy.expose
    def welcome(self):
        global config

        if (config.WARNING == 1):
            with open("html/warning.html", "r") as myfile:
                retString = myfile.read()
        else:
            with open("html/welcome.html", "r") as myfile:
                retString = myfile.read()

        return retString

    @cherrypy.expose
    def register_list(self):
        global REGS_LIST

        maxSize = 0
        for register in REGS_LIST:
            if (len(register.name) > maxSize):
                maxSize = len(register.name)
        # make an array of html strings to describe the buttons
        sButtonArray = []
        sButtonArray.append("""  <div style="text-align: left; "> """)
        for register in REGS_LIST:
            sButtonArray.append(
                """         <button style="width:200px; height:60px; vertical-align:middle; display:inline; margin: 3px 5px 3px 5px;" onclick='javascript:load_register("%s", "true", "none", "none")'>%s</button>""" % (
                register.name.replace(" ", "_").encode('ascii', 'ignore'), register.name))

        sButtonArray.append("""  </div> """)
        sButtonInsert = "".join(sButtonArray)

        return sButtonInsert

    @cherrypy.expose
    def hifunction_list(self):
        global FUNC_LIST
        # make an array of html strings to describe the buttons
        sButtonArray = []
        sButtonArray.append("""  <div style="text-align: left;"> """)
        for func in FUNC_LIST:
            sButtonArray.append(
                """         <button style="width:100px; height:60px; vertical-align:middle; display:inline; margin: 3px 5px 3px 5px;" onclick='javascript:load_hifunction("%s", true, "none", "none")'>%s</button>""" % (
                func.name.replace(" ", "_").encode('ascii', 'ignore'), func.name))

        sButtonArray.append("""  </div> """)
        sButtonInsert = "".join(sButtonArray)

        return sButtonInsert

    @cherrypy.expose
    def sidebar_silent(self):
        # make an array of html strings to describe the buttons
        retval = """
    <button style="display:block" id="sidebar_welcome" class="sidebar_list"> Welcome </button>
    <button style="display:block" id="sidebar_configure" class="sidebar_list" > Configure </button>
    <button style="display:block" id="sidebar_firmware_update (I2C)" class="sidebar_list" > Host Interface FW Update </button>
    <button style="display:block" id="sidebar_firmware_update (SPI)" class="sidebar_list" > SPI FW Update </button>
    <button style="display:block" id="sidebar_register_list" class="sidebar_list"  > Register List </button>
    <button style="display:block" id="sidebar_host_interface_commands" class="sidebar_list" > Command List </button>
    """

        return retval

    @cherrypy.expose
    def sidebar_disabled(self):
        # make an array of html strings to describe the buttons
        retval = """
    <button style="display:block" id="sidebar_welcome" class="sidebar_list" onclick="Javascript:jsFlashingClickError()" > Welcome </button>
    <button style="display:block" id="sidebar_configure" class="sidebar_list" onclick="Javascript:jsFlashingClickError()" > Configure </button>
    <button style="display:block" id="sidebar_firmware_update (I2C)" class="sidebar_list" onclick="Javascript:jsFlashingClickError()"> Host Interface FW Update </button>
    <button style="display:block" id="sidebar_firmware_update (SPI)" class="sidebar_list" onclick="Javascript:jsFlashingClickError()"> SPI FW Update </button>
    <button style="display:block" id="sidebar_register_list" class="sidebar_list" onclick="Javascript:jsFlashingClickError()" > Register List </button>
    <button style="display:block" id="sidebar_host_interface_commands" class="sidebar_list" onclick="Javascript:jsFlashingClickError()" > Command List </button>
    """

        return retval

    @cherrypy.expose
    def sidebar(self):
        # make an array of html strings to describe the buttons
        retval = """
    <button style="display:block" id="sidebar_welcome" class="sidebar_list" onclick="Javascript:load_welcome()" onmouseover="this.style.color='#000';" onmouseout="this.style.color='#cc0000';"> Welcome </button>
    <button style="display:block" id="sidebar_configure" class="sidebar_list" onclick="Javascript:load_config()" onmouseover="this.style.color='#000';" onmouseout="this.style.color='#cc0000';" > Configure </button>
    <button style="display:block" id="sidebar_firmware_update (I2C)" class="sidebar_list" onclick="Javascript:load_update_iic()" onmouseover="this.style.color='#000';" onmouseout="this.style.color='#cc0000';"> Host Interface FW Update </button>
    <button style="display:block" id="sidebar_firmware_update (SPI)" class="sidebar_list" onclick="Javascript:load_update_spi()" onmouseover="this.style.color='#000';" onmouseout="this.style.color='#cc0000';"> SPI FW Update </button>
    <button style="display:block" id="sidebar_register_list" class="sidebar_list" onclick="Javascript:load_register_list()"  onmouseover="this.style.color='#000';" onmouseout="this.style.color='#cc0000';"> Register List </button>
    <button style="display:block" id="sidebar_host_interface_commands" class="sidebar_list" onclick="Javascript:load_hifunction_list()"  onmouseover="this.style.color='#000';" onmouseout="this.style.color='#cc0000';"> Command List </button>
    """

        return retval

    @cherrypy.expose
    def config_handler(self, confname, value):
        global config
        global handle

        cherrypy.response.headers['Content-Type'] = 'application/json'
        returnDict = {'failure': 0, 'failure_message': 'No failure'}

        try:
            # be sure to close any live connection before updating settings.
            handle.hw_close()

            if confname == 'Hw_int':
                config.HW_INTERFACE = int(value)
            elif confname == 'IIC_addr':
                if value[:2] == '0x':
                    config.DEVICE_I2C_ADDR = int(value[2:], 16)
                else:
                    config.DEVICE_I2C_ADDR = int(value, 10)
                handle.hw_set_i2c_addr(config.DEVICE_I2C_ADDR)
            elif confname == 'bitrate':
                config.BITRATE = int(value)
            elif confname == 'spibitrate':
                config.SPIBITRATE = int(value)
            elif confname == 'port':
                config.PORT = int(value)
            elif confname == 'spi_port':
                config.SPI_PORT = int(value)
            elif confname == 'update':
                confString = ""
                with open("html\config_template.py", "r") as myfile:
                    confString = myfile.read()
                confString = confString.replace('**HW_INT**', str(config.HW_INTERFACE))
                confString = confString.replace('**IIC_ADDR**', '0x%x' % config.DEVICE_I2C_ADDR)
                confString = confString.replace('**BR**', str(config.BITRATE))
                confString = confString.replace('**SBR**', str(config.SPIBITRATE))
                confString = confString.replace('**PRT**', str(config.PORT))
                confString = confString.replace('**SPIPRT**', str(config.SPI_PORT))
                confString = confString.replace('**WRNG**', str(config.WARNING))
                with open("config.py", "w") as myfile2:
                    myfile2.write(confString)
                handle.hw_set_i2c_addr(config.DEVICE_I2C_ADDR)

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            handle.hw_close()
            returnDict['failure'] = 1
            returnDict['failure_message'] = "Configuration Page Exception:\n"
            returnDict['failure_message'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            return simplejson.dumps(returnDict)

    @cherrypy.expose
    def config_test(self):
        global config
        global handle
        global connected

        retString = "<p> Connection Results: <p>"

        try:
            handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                           config.DEVICE_I2C_ADDR)

            retString += "<p>Successful Interface Open</p>"

            MODE_REG.read(handle)
            connected = True
            handle.hw_close()

            retString += """Attempt to read Mode Register succeeded<br>"""
            modeString = ""
            for modeField in MODE_REG.fields:
                modeString += modeField.translate(modeField)
            retString += "Mode Register returns: %s" % modeString
            return retString

        except Exception as myExc:
            e = sys.exc_info()
            handle.hw_close()
            retString += """<h1>Exception Encountered during Configure Test</h1>"""
            retString += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            connected = False
            return retString

    @cherrypy.expose
    def config(self):
        global config
        retString = "<h1>USB to I2C/SPI Adapter Configuration</h1>"
        retString += """         <button style="display:inline" onclick="javascript:jsConfigHandler(this, \'update\')">Save Settings as Default</button>"""
        retString += """ <hr size='1px' color="#aaaaaa" noshade style="margin-top: 15px; margin-bottom: 15px"> """
        retString += "<table><tr><td> USB to I2C/SPI Adapter </td>"
        retString += """<td align="right"><select value=%d onchange="jsConfigHandler(this, \'Hw_int\')"> \n""" % (
            config.HW_INTERFACE)
        for item in config.HW_INT_DICT:
            if (config.HW_INTERFACE == config.HW_INT_DICT[item]):
                retString += '    <option value=%d selected="selected">%s</option> \n' % (
                config.HW_INT_DICT[item], item)
            else:
                retString += '    <option value=%d>%s</option> \n' % (config.HW_INT_DICT[item], item)
        retString += '</select> </td> </tr>\n'

        retString += "<tr><td> Device I2C Address </td>"
        retString += '<td align="right"> <input type="text" value="0x%x" size="%d" onchange="jsConfigHandler(this, \'IIC_addr\')"> </td> </tr>\n' % (
        config.DEVICE_I2C_ADDR, len(str("0x%x" % config.DEVICE_I2C_ADDR)) + 2)

        retString += "<tr><td> I2C Bitrate </td>"
        retString += """<td align="right"><select value=%d onchange="jsConfigHandler(this, \'bitrate\')"> \n""" % (
            config.BITRATE)
        for item in config.BITRATE_DICT:
            if (config.BITRATE == config.BITRATE_DICT[item]):
                retString += '    <option value=%d selected="selected">%s</option> \n' % (
                config.BITRATE_DICT[item], item)
            else:
                retString += '    <option value=%d>%s</option> \n' % (config.BITRATE_DICT[item], item)
        retString += '</select> </td> </tr>\n'

        retString += "<tr><td> SPI Bitrate </td>"
        retString += """<td align="right"><select value=%d onchange="jsConfigHandler(this, \'spibitrate\')"> \n""" % (
            config.SPIBITRATE)
        for item in config.SPIBITRATE_DICT:
            if (config.SPIBITRATE == config.SPIBITRATE_DICT[item]):
                retString += '    <option value=%d selected="selected">%s</option> \n' % (
                config.SPIBITRATE_DICT[item], item)
            else:
                retString += '    <option value=%d>%s</option> \n' % (config.SPIBITRATE_DICT[item], item)
        retString += '</select> </td> </tr>\n'

        retString += "<tr><td> I2C Port </td>"
        retString += """<td align="right"><select value=%d onchange="jsConfigHandler(this, \'port\')"> \n""" % (
            config.PORT)
        for item in config.PORT_DICT:
            if (config.PORT == config.PORT_DICT[item]):
                retString += '    <option value=%d selected="selected">%s</option> \n' % (config.PORT_DICT[item], item)
            else:
                retString += '    <option value=%d>%s</option> \n' % (config.PORT_DICT[item], item)
        retString += '</select> </td> </tr>\n'

        retString += "<tr><td> SPI Port </td>"
        retString += """<td align="right"><select value=%d onchange="jsConfigHandler(this, \'spi_port\')"> \n""" % (
            config.SPI_PORT)
        for item in config.PORT_DICT:
            if (config.SPI_PORT == config.PORT_DICT[item]):
                retString += '    <option value=%d selected="selected">%s</option> \n' % (config.PORT_DICT[item], item)
            else:
                retString += '    <option value=%d>%s</option> \n' % (config.PORT_DICT[item], item)
        retString += '</select> </td> </tr>\n'

        retString += '</table>\n'

        retString += """ <hr size='1px' color="#aaaaaa" noshade style="margin-top: 15px; margin-bottom: 15px"> """
        retString += """         <button style="display:inline" onclick="javascript:jsConfigTestHandler(this)">Test Configuration Settings</button>"""
        retString += """         <div id="idConfigTest"></div>"""

        return retString

    @cherrypy.expose
    def spi_upload_file_startpage(self):
        retString = """<h1>SPI Flash Update</h1>"""
        retString += """<button id="abortButton">Abort Flash Update</button>"""
        retString += "<h2> Updating flash image in progress... </h2>"
        retString += """<div id="spi_flashing_message"></div>"""

        return retString

    @cherrypy.expose
    def upload_file_abort(self):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        returnDict = {'failure': 0, 'failure_message': 'No failure'}

        global flashAbort
        flashAbort = 1

        i2cvariables['error_msg'] = "Flash Abort (User Input)"

        return simplejson.dumps(returnDict)

    @cherrypy.expose
    def upload_file_abort_page(self):
        global flashAbort
        flashAbort = 1

        retString = "<h1>I2C Flash Update Aborted</h1>"

        retString += convtohtml(i2cvariables['error_msg']);

        return retString

    @cherrypy.expose
    def spi_upload_file_abort(self):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        returnDict = {'failure': 0, 'failure_message': 'No failure'}

        global spivariables
        global spiFlashAbort
        spiFlashAbort = 1

        spivariables['error_msg'] = "Flash Abort (User Input)"

        return simplejson.dumps(returnDict)

    @cherrypy.expose
    def spi_upload_file_abort_page(self):
        global spivariables

        retString = "<h1>SPI Flash Update Aborted</h1>"
        retString += convtohtml(spivariables['error_msg']);

        return retString

    @cherrypy.expose
    def upload_file_progbar_init(self):
        global flashAbort
        global region_pointer
        global rp_select
        global rp0
        global rp1
        global i2cvariables
        global config
        global connected
        global handle

        try:
            i2cvariables['sector'] = 0
            i2cvariables['numBlocks'] = 0
            i2cvariables['count'] = 0
            i2cvariables['length'] = len(filedata)
            i2cvariables['error_msg'] = "Unknown Error"

            Ace_ID_Value = 0xACE00001

            flashAbort = 0

            abortMessage = """<h2>Flash update Aborted</h2>"""

            retString = """<h1>I2C Flash Update</h1>"""
            retString += """<button id="abortButton">Abort Flash Update</button>"""
            retString += "<h2> Flashing region %d in progress... </h2>" % rp_select

            if (len(filedata) < 4):
                retString += """<h1>Input file is not a valid low-region file</h1>"""
                retString += """<p>A low region files is an application binary (max 64k) with a prepended 4k boot header. </p>"""
                flashAbort = 1
                retString += abortMessage
                return retString

            if (((filedata[3] << 24) | (filedata[2] << 16) | (filedata[1] << 8) | filedata[0]) != Ace_ID_Value):
                retString += """<h1>Input file is not a valid low-region file</h1>"""
                retString += """<p>A low region files is an application binary (max 64k) with a prepended 4k boot header. </p>"""
                flashAbort = 1
                retString += abortMessage
                return retString

            if (flashAbort == 0):
                handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                               config.DEVICE_I2C_ADDR)
            else:
                handle.hw_close()
                i2cvariables['numBlocks'] = -1
                retString += abortMessage
                return retString

            if (rp_select == 0):
                region_pointer = rp0
            elif (rp_select == 1):
                region_pointer = rp1
            else:
                retString += """<h1>Improper Region Pointer Selection</h1>"""
                flashAbort = 1
                retString += abortMessage
                return retString

            retString += """<p>Erasing region</p>"""
            retString += """<div id="i2cflash_erase_progbar_insert"></div>"""
            retString += """<p id="i2cflash_write_message"></p>"""
            retString += """<div id="i2cflash_write_progbar_insert"></div>"""
            retString += """<p id="i2cflash_verification_message"></p>"""

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            i2cvariables['error_msg'] = """Exception Encountered during I2C Upload Initialization\n"""
            i2cvariables['error_msg'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            (status, message) = handle.hw_close()
            if status != 0:
                i2cvariables['error_msg'] += "Error encountered during adapter close:\n"
                i2cvariables['error_msg'] += message
            flashAbort = 1
            retString += i2cvariables['error_msg']
            retString += abortMessage
            connected = False
            return retString

    @cherrypy.expose
    def upload_file_progbar_erase(self):
        global region_file
        global filedata
        global flashAbort
        global region_pointer
        global i2cvariables
        global abortMessage
        global connected

        cherrypy.response.headers['Content-Type'] = 'application/json'
        returnDict = {'erase_size': 17, 'progress': i2cvariables['sector'], 'error_msg': ""}
        abortMessage = """<h2>Flash update Aborted</h2>"""

        try:
            # first call return without erasing to setup progress bar
            if (i2cvariables['sector'] == 0):
                i2cvariables['sector'] = 1
                return simplejson.dumps(returnDict)

            # Should never get here if Javascript shell working properly
            # but if we do, keep from erasing too far
            if (i2cvariables['sector'] > 17):
                return simplejson.dumps(returnDict)

            if (flashAbort == 0):
                # erase region
                # Max image size is 64K plus a 4K header = 17 sectors
                FLem(handle, region_pointer + ((i2cvariables['sector'] - 1) * 0x1000), 1)
                i2cvariables['sector'] = i2cvariables['sector'] + 1
                if (i2cvariables['sector'] > 17):
                    return simplejson.dumps(returnDict)

                FLem(handle, region_pointer + ((i2cvariables['sector'] - 1) * 0x1000), 1)
                i2cvariables['sector'] = i2cvariables['sector'] + 1
                if (i2cvariables['sector'] > 17):
                    return simplejson.dumps(returnDict)

                FLem(handle, region_pointer + ((i2cvariables['sector'] - 1) * 0x1000), 1)
                i2cvariables['sector'] = i2cvariables['sector'] + 1
                if (i2cvariables['sector'] > 17):
                    return simplejson.dumps(returnDict)

                FLem(handle, region_pointer + ((i2cvariables['sector'] - 1) * 0x1000), 1)
                i2cvariables['sector'] = i2cvariables['sector'] + 1
                if (i2cvariables['sector'] > 17):
                    return simplejson.dumps(returnDict)


            else:
                i2cvariables['sector'] = -1
                (status, message) = handle.hw_close()
                if status != 0:
                    i2cvariables['error_msg'] += "Error encountered during adapter close:\n"
                    i2cvariables['error_msg'] += message
                return simplejson.dumps({'erase_size': -1, 'progress': -1, 'error_msg': i2cvariables['error_msg']})

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            connected = False
            i2cvariables['sector'] = -1
            flashAbort = 1
            i2cvariables['error_msg'] = """Exception Encountered during I2C Flash Erase\n"""
            i2cvariables['error_msg'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            (status, message) = handle.hw_close()
            if status != 0:
                i2cvariables['error_msg'] += "Error encountered during adapter close:\n"
                i2cvariables['error_msg'] += message
            return simplejson.dumps({'erase_size': -1, 'progress': -1, 'error_msg': i2cvariables['error_msg']})

    @cherrypy.expose
    def upload_file_progbar_write(self):
        global flashAbort
        global i2cvariables
        global connected
        global filedata
        global region_pointer
        PAGE_SIZE = 64

        cherrypy.response.headers['Content-Type'] = 'application/json'
        returnDict = {'write_size': i2cvariables['length'],
                      'progress': ((i2cvariables['numBlocks'] * 64) + i2cvariables['count']) * 64}
        abortMessage = """<h2>Flash update Aborted</h2>"""

        # first call return without erasing to setup progress bar
        try:
            if ((i2cvariables['numBlocks'] == 0) and (i2cvariables['count'] == 0)):
                if (flashAbort == 0):
                    # set start address for region
                    FLad(handle, region_pointer)

                    # Write the data to the bus
                    data1 = array('B', filedata[0:PAGE_SIZE])

                    del filedata[0:PAGE_SIZE]

                    FLwd(handle, data1)

                    i2cvariables['count'] = 1
                    return simplejson.dumps(returnDict)
                else:
                    (status, message) = handle.hw_close()
                    if status != 0:
                        i2cvariables['error_msg'] += "Error encountered during adapter close:\n"
                        i2cvariables['error_msg'] += message
                    numBlocks = -1
                    return simplejson.dumps({'write_size': -1, 'progress': -1})

            # Write the data to the bus
            for i in range(32):
                data1 = array('B', filedata[0:PAGE_SIZE])

                del filedata[0:PAGE_SIZE]

                length = len(data1)
                if ((length == 0)):
                    return simplejson.dumps({'write_size': i2cvariables['length'], 'progress': i2cvariables['length']})

                if (flashAbort != 0):
                    handle.hw_close()
                    numBlocks = -1
                    return simplejson.dumps({'write_size': -1, 'progress': -1})

                FLwd(handle, data1)

                i2cvariables['count'] += 1
                if (i2cvariables['count'] == 64):
                    i2cvariables['numBlocks'] += 1
                    i2cvariables['count'] = 0

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            connected = False
            i2cvariables['numblocks'] = -1
            i2cvariables['count'] = -1
            flashAbort = 1
            i2cvariables['error_msg'] = """Exception Encountered during I2C Flash Write\n"""
            i2cvariables['error_msg'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            (status, message) = handle.hw_close()
            if status != 0:
                i2cvariables['error_msg'] += "Error encountered during adapter close:\n"
                i2cvariables['error_msg'] += message
            return simplejson.dumps({'write_size': -1, 'progress': -1, 'error_msg': i2cvariables['error_msg']})

    @cherrypy.expose
    def upload_file_progbar_verify(self):
        global flashAbort
        global rp_select
        global i2cvariables
        global region_pointer
        global rp_select
        global handle
        global connected

        abortMessage = """<h2>Flash update Aborted</h2>"""

        try:
            retString = "<p>Programming of region %d complete</p>" % rp_select

            retString += "<p>Updating Region Pointer Record</p>"

            region_record_ptr = 0x0;

            # Erase region data record
            if (rp_select == 0):
                region_record_ptr = 0x0
            elif (rp_select == 1):
                region_record_ptr = 0x1000

            if (flashAbort == 0):
                FLem(handle, region_record_ptr, 1)
            else:
                handle.hw_close()
                i2cvariables['numBlocks'] = -1
                return abortMessage

            # write in the region pointers
            rpblock = array('B')

            for i in range(64):
                rpblock.append(0xFF)

            rpoffset = region_pointer - 0x2000

            rpblock[0] = 0x00
            rpblock[1] = 0x20
            rpblock[2] = 0x00
            rpblock[3] = 0x00

            if (flashAbort == 0):
                FLad(handle, region_record_ptr)
                FLwd(handle, rpblock)
            else:
                handle.hw_close()
                i2cvariables['numBlocks'] = -1
                return abortMessage

            rpblock[0] = 0xFF
            rpblock[1] = 0xFF
            rpblock[2] = 0xFF
            rpblock[3] = 0xFF

            rpblock[60] = rpoffset & 0xFF
            rpblock[61] = (rpoffset >> 8) & 0xFF
            rpblock[62] = (rpoffset >> 16) & 0xFF
            rpblock[63] = (rpoffset >> 24) & 0xFF

            if (flashAbort == 0):
                FLad(handle, region_record_ptr + 0x1000 - 0x40)
                FLwd(handle, rpblock)
            else:
                handle.hw_close()
                i2cvariables['numBlocks'] = -1
                return abortMessage

            if (flashAbort == 0):
                # verify boot sequence using FLrr and FLvy
                region_pointer = FLrr(handle, rp_select)
                failure = FLvy(handle, region_pointer)
                connected = True
            else:
                handle.hw_close()
                i2cvariables['numBlocks'] = -1
                return abortMessage

            if failure != 0:
                retString += '<p>Verification of region %d FAILED</p>' % rp_select
                retString += '<p>With failure code %d<p>' % failure
            else:
                retString += '<p>Verification of region %d SUCCEEDED</p>' % rp_select

            # Close the device
            handle.hw_close()

            # numBlocks = -1 tells master page to stop querying for updates
            i2cvariables['numBlocks'] = -1

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            connected = False
            i2cvariables['numblocks'] = -1
            i2cvariables['count'] = -1
            flashAbort = 1
            i2cvariables['error_msg'] = """Exception Encountered during I2C Flash Verify\n"""
            i2cvariables['error_msg'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            (status, message) = handle.hw_close()
            if status != 0:
                i2cvariables['error_msg'] += "Error encountered during adapter close:\n"
                i2cvariables['error_msg'] += message
            retString += i2cvariables['error_msg']
            return retString

    @cherrypy.expose
    def spi_upload_file_init(self):
        Ace_ID_Value = 0xACE00001
        global spifiledata
        global spiFlashAbort
        global spivariables
        global spiFlashError
        global numSpiBlocks
        global config
        global connected

        try:
            abortMessage = """<h1>Flash update Aborted</h2>"""

            spivariables['sector'] = 0
            spivariables['count'] = 0
            spivariables['addr'] = 0
            spivariables['posn'] = 0
            spivariables['length'] = len(spifiledata)
            spivariables['compval'] = True
            spivariables['error_msg'] = "Unknown error encountered"

            spiFlashAbort = 0

            retString = """<h1>SPI Flash Update</h1>"""
            retString += """<button id="spiAbortButton">Abort Flash Update</button>"""
            retString += "<h2> Updating flash image in progress... </h2>"

            handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                           config.DEVICE_I2C_ADDR)

            retString += """<p>Erasing 1M Flash</p>"""
            retString += """<div id="spiflash_erase_progbar_insert"></div>"""
            retString += """<p id="spiflash_write_message"></p>"""
            retString += """<div id="spiflash_write_progbar_insert"></div>"""
            retString += """<p id="spiflash_verification_message"></p>"""
            retString += """<div id="spiflash_verify_progbar_insert"></div>"""
            retString += """<p id="spiflash_verification_result"></p>"""

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            connected = False
            spivariables['error_msg'] = "Exception Encountered during SPI Upload Initialization:\n"
            spivariables['error_msg'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            spiFlashAbort = 1
            retString += abortMessage
            (status, message) = handle.hw_close()
            if status != 0:
                spivariables['error_msg'] += "Error encountered while closing adapter:\n"
                spivariables['error_msg'] += message
            numSpiBlocks = -1
            retString += spivariables['error_msg']
            return retString

    @cherrypy.expose
    def spi_upload_file_erase(self):
        Ace_ID_Value = 0xACE00001
        global spifiledata
        global spiFlashAbort
        global spivariables
        global connected

        try:

            cherrypy.response.headers['Content-Type'] = 'application/json'
            returnDict = {'erase_size': 255, 'progress': spivariables['sector'], 'error_msg': ""}

            for i in range(16):
                if (spiFlashAbort == 0):
                    # erase 1M flash
                    # 1M / 4K = 255
                    if (spivariables['sector'] < 255):
                        handle.hw_spi_flash_erase(0x0 + (spivariables['sector'] - 1) * 0x1000, 1)
                        spivariables['sector'] = spivariables['sector'] + 1

                    else:
                        returnDict = {'write_size': 255, 'progress': 255}
                        handle.hw_spi_flash_erase(0x0 + (spivariables['sector'] - 1) * 0x1000, 1)

                else:
                    handle.hw_close()
                    return simplejson.dumps({'erase_size': -1, 'progress': -1, 'error_msg': spivariables['error_msg']})

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            connected = False
            spivariables['error_msg'] = "Exception encountered during spi flash erase:\n"
            spivariables['error_msg'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            (status, message) = handle.hw_close()
            if status != 0:
                spivariables['error_msg'] += "Error encountered during adapter module close:\n"
                spivariables['error_msg'] += message
            returnDict['error_msg'] = spivariables['error_msg']
            returnDict['erase_size'] = -1
            returnDict['progress'] = -1
            spiFlashAbort = 1

            return simplejson.dumps(returnDict)

    @cherrypy.expose
    def spi_upload_file_write(self):
        Ace_ID_Value = 0xACE00001
        global spifiledata
        global spiFlashAbort
        global spivariables
        global connected

        try:

            cherrypy.response.headers['Content-Type'] = 'application/json'
            returnDict = {'write_size': spivariables['length'], 'progress': spivariables['addr'], 'error_msg': ""}

            if spivariables['count'] == 0:
                # first iteration is just used to initialize progress bar
                spivariables['count'] = 1
                return simplejson.dumps(returnDict)

            for i in range(32):
                # Write the data to the bus
                length = spivariables['length'] - spivariables['addr']

                data1 = array('B', spifiledata[spivariables['addr']:spivariables['addr'] + handle.spiPageSize])

                # truncate array to exact size
                if (length < handle.spiPageSize):
                    del data1[length:]
                    if (length > 0):
                        for i in range(length, handle.spiPageSize):
                            data1.append(0xFF)
                    else:
                        del data1
                        data1 = array('B')

                # Write the data to the bus
                if (spiFlashAbort == 0):
                    if (len(data1) > 0):
                        handle.hw_spi_write(spivariables['addr'], data1)

                else:
                    handle.hw_close()
                    spivariables['addr'] = -1
                    returnDict = {'write_size': -1, 'progress': -1, 'error_msg': spivariables['error_msg']}
                    return simplejson.dumps(returnDict)

                spivariables['addr'] += len(data1)

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            connected = False
            spivariables['error_msg'] = "Exception encountered during spi flash write:\n"
            spivariables['error_msg'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            (status, message) = handle.hw_close()
            if status != 0:
                spivariables['error_msg'] += "Error encountered during adapter module close:\n"
                spivariables['error_msg'] += message
            returnDict['error_msg'] = spivariables['error_msg']
            returnDict['write_size'] = -1
            returnDict['progress'] = -1
            spiFlashAbort = 1
            return simplejson.dumps(returnDict)

    @cherrypy.expose
    def spi_upload_file_verify(self):
        global spifiledata
        global spiFlashAbort
        global spivariables
        global connected

        try:
            cherrypy.response.headers['Content-Type'] = 'application/json'
            returnDict = {'verify_size': spivariables['length'], 'progress': spivariables['posn']}

            # first call just initializes the progress bar
            if spivariables['count'] == 1:
                spivariables['count'] = 2
                return simplejson.dumps(returnDict)

            for i in range(32):
                length = spivariables['length'] - spivariables['posn']

                # Write the data to the bus
                data1 = array('B', spifiledata[spivariables['posn']:spivariables['posn'] + handle.spiPageSize])

                # Truncate the array to the exact data size
                if (length < handle.spiPageSize):
                    del data1[length:]

                # Reread data
                if (spiFlashAbort == 0):
                    (count, readcomp) = handle.hw_spi_read(spivariables['posn'], len(data1))
                    connected = True

                else:
                    spivariables['posn'] = -1
                    spiFlashAbort = 1
                    spivariables['error_msg'] = "Flash Update Aborted (user input)\n"
                    (status, message) = handle.hw_close()
                    if status != 0:
                        spivariables['error_msg'] += "adapter close command failed with error message:\n"
                        spivariables['error_msg'] += message
                    returnDict = {'verify_size': -1, 'progress': -1, 'error_msg': spivariables['error_msg']}
                    return simplejson.dumps(returnDict)

                if (count != len(data1)):
                    connected = False
                    spivariables['posn'] = -1
                    spiFlashAbort = 1
                    spivariables['error_msg'] = "Flash Update Aborted (read failure)\n"
                    (status, message) = handle.hw_close()
                    if status != 0:
                        spivariables['error_msg'] += "adapter close command failed with error message:\n"
                        spivariables['error_msg'] += message
                    returnDict = {'verify_size': -1, 'progress': -1, 'error_msg': spivariables['error_msg']}
                    return simplejson.dumps(returnDict)

                for i in range(len(data1)):
                    if (data1[i] != readcomp[i]):
                        spivariables['compval'] = False

                spivariables['posn'] += len(data1)

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            connected = False
            spivariables['error_msg'] = "Exception occurred during spi flash verify:\n"
            spivariables['error_msg'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            (status, message) = handle.hw_close()
            if status != 0:
                spivariables['error_msg'] += "adapter close command failed with error message:\n"
                spivariables['error_msg'] += message
            returnDict['error_msg'] = spivariables['error_msg']
            returnDict['verify_size'] = -1
            returnDict['progress'] = -1
            spiFlashAbort = 1
            return simplejson.dumps(returnDict)

    @cherrypy.expose
    def spi_upload_file_result(self):
        global spifiledata
        global spiFlashAbort
        global spivariables
        global connected

        try:
            # Close the device
            handle.hw_close()

            if spivariables['compval'] == True:
                retString = """<p>Flash verification succeeded</p>"""
            else:
                retString = """<p>Flash verification failed</p>"""

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            connected = False
            retString += "<h1>Exception Encountered during SPI Upload </h1>"
            retString += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            spiFlashAbort = 1
            return retString

    @cherrypy.expose
    def handle_update_iic(self, variable, value):
        global rp0
        global rp1
        global rp_select

        try:
            cherrypy.response.headers['Content-Type'] = 'application/json'
            returnDict = {'failure': 0, 'failure_message': 'No failure'}

            if variable == 'rp0':
                if value[:2] == '0x':
                    rp0 = int(value, 16)
                else:
                    rp0 = int(value)

            if variable == 'rp1':
                if value[:2] == '0x':
                    rp1 = int(value, 16)
                else:
                    rp1 = int(value)

            if variable == 'rp_select':
                rp_select = int(value)

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            returnDict['failure'] = 1
            returnDict['failure_message'] = """Exception encountered during update I2C:\n"""
            returnDict['failure_message'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            return simplejson.dumps(returnDict)

    @cherrypy.expose
    def handle_update_flashfile(self, dataURL):
        global filedata
        try:
            cherrypy.response.headers['Content-Type'] = 'application/json'
            returnDict = {'failure': 0, 'failure_message': 'No failure'}

            filedata = bytearray()
            for value in dataURL:
                filedata.append(ord(value))

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            returnDict['failure'] = 1
            returnDict['failure_message'] = """Exception encountered during update I2C flash file:\n"""
            returnDict['failure_message'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            return simplejson.dumps(returnDict)

    @cherrypy.expose
    def handle_update_spiflashfile(self, dataURL):
        global spifiledata
        try:
            cherrypy.response.headers['Content-Type'] = 'application/json'
            returnDict = {'failure': 0, 'failure_message': 'No failure'}

            spifiledata = bytearray()
            for value in dataURL:
                spifiledata.append(ord(value))

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            returnDict['failure'] = 1
            returnDict['failure_message'] = """Exception encountered during update SPI flash file:\n"""
            returnDict['failure_message'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            return simplejson.dumps(returnDict)

    @cherrypy.expose
    def update_iic_preview(self):
        try:
            retString = """<h1>I2C (Host Interface) Region 0/1 Flash Update</h1>"""

            retString += """<p>Region 0 Start Address</p>"""
            retString += '<input type="text" value="%s" >' % str("loading")

            retString += """<p>Region 1 Start Address</p>"""
            retString += '<input type="text" value="%s" >' % str("loading")

            retString += """<p>Choose Region to Program</p>"""
            retString += """<select value=%d > \n""" % (rp_select)
            if (rp_select == 0):
                retString += '    <option value=0 selected="selected">Region 0</option> \n'
                retString += '    <option value=1>Region 1</option> \n'
            else:
                retString += '    <option value=0>Region 0</option> \n'
                retString += '    <option value=1 selected="selected">Region 1</option> \n'
            retString += '</select> \n'

            retString += """<p> Low-region File to Write </p> 
                            <input style="font-size: 20px; height: 30px; width: 100%" type="file" id="flashFile" size="40">
                            <p id="flash_button_insert">(Load File to Proceed)</p>"""

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            retString += """<h2>Exception encountered during update I2C:</h2>"""
            retString += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            return retString

    @cherrypy.expose
    def update_iic(self):
        global connected
        global rp0
        global rp1
        global rp_select
        global config

        try:
            retString = """<h1>I2C (Host Interface) Region 0/1 Flash Update</h1>"""

            handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                           config.DEVICE_I2C_ADDR)

            rp0 = FLrr(handle, 0)
            rp1 = FLrr(handle, 1)
            connected = True
            handle.hw_close()

            if rp0 < 0x2000:
                rp0 = 0x2000

            if rp1 < 0x2000:
                rp1 = 0x2000

            retString += """<p>Region 0 Start Address</p>"""
            retString += '<input type="text" value="%s" onchange="jsUpdateIicHandler(this, \'rp0\')">' % str(
                translateRegPtr(rp0))

            retString += """<p>Region 1 Start Address</p>"""
            retString += '<input type="text" value="%s" onchange="jsUpdateIicHandler(this, \'rp1\')">' % str(
                translateRegPtr(rp1))

            retString += """<p>Choose Region to Program</p>"""
            retString += """<select value=%d onchange="jsUpdateIicHandler(this, \'rp_select\')"> \n""" % (rp_select)
            if (rp_select == 0):
                retString += '    <option value=0 selected="selected">Region 0</option> \n'
                retString += '    <option value=1>Region 1</option> \n'
            else:
                retString += '    <option value=0>Region 0</option> \n'
                retString += '    <option value=1 selected="selected">Region 1</option> \n'
            retString += '</select> \n'

            retString += """<p> Low-region File to Write </p> 
                            <input style="font-size: 20px; height: 30px; width: 100%" type="file" id="flashFile" size="40" onchange="jsUpdateFlashFile()">
                            <p id="flash_button_insert">(Load File to Proceed)</p>"""

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            retString += """<h1>Exception Occured during I2C update:</h1>"""
            retString += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            connected = False
            handle.hw_close()
            return retString

    @cherrypy.expose
    def update_spi(self):
        try:
            retString = """<h1>SPI (Direct Flash) Full Flash Update</h1>"""

            if config.HW_INTERFACE == config.HW_INT_DICT['USB EP']:
                retString += """ <p> SPI Flash Update is not supported using USB2.0 Endpoint </p>
                <p>Please use the Host Interface FW Update utility instead.</p>
                <p>Or reconfigure to use another debugging interface.</p>
                """
                return retString

            retString += """<p> Flash Image File to Write </p>
                            <p> Must contain a full flash image with region pointers and boot headers </p> 
                            <input style="font-size: 20px; height: 30px; width: 100%" type="file" id="spiFlashFile" size="40" onchange="jsUpdateSpiFlashFile()">
                            <p id="spi_flash_button_insert">(Load File to Proceed)</p>"""

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            retString += """<h1>Exception Occured during SPI update:</h1>"""
            retString += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            return retString

    @cherrypy.expose
    def submit(self, register, field, value):
        try:
            cherrypy.response.headers['Content-Type'] = 'application/json'
            returnDict = {'failure': 0, 'failure_message': 'No failure'}
            myRegister = registerByName(register.replace("_", " ").encode('ascii', 'ignore'))
            myField = myRegister.fields[int(field)]

            if ((myField.translate == register_class.listTranslate) or ('Supply Type' in myField.name)):
                myField.value = int(value)
            else:
                myField.value = myField.reversetranslate(myField, value)

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            returnDict['failure'] = 1
            returnDict['failure_message'] = """Exception Occured during register field update:\n"""
            returnDict['failure_message'] += """field name is %s""" % myField.name
            returnDict['failure_message'] += """revtranslate is %d""" % myField.reversetranslate(myField, str(value))
            returnDict['failure_message'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            return simplejson.dumps(returnDict)

    @cherrypy.expose
    def infunc(self, func, field, value):
        try:
            cherrypy.response.headers['Content-Type'] = 'application/json'
            returnDict = {'failure': 0, 'failure_message': 'No failure'}
            myFunction = functionByName(func.replace("_", " ").encode('ascii', 'ignore'))
            myField = myFunction.inputs[int(field)]

            if ((myField.translate == listTranslate) or ('Supply Type' in myField.name)):
                myField.value = int(value)
            else:
                myField.value = myField.reversetranslate(myField, value)

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            returnDict['failure'] = 1
            returnDict['failure_message'] = """Exception Occured during register field update:\n"""
            returnDict['failure_message'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            return simplejson.dumps(returnDict)

    @cherrypy.expose
    def write(self, register):
        global handle
        global connected
        global config

        try:
            cherrypy.response.headers['Content-Type'] = 'application/json'
            returnDict = {'failure': 0, 'failure_message': 'No failure'}

            myRegister = registerByName(register.replace("_", " ").encode('ascii', 'ignore'))

            handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                           config.DEVICE_I2C_ADDR)

            myRegister.write(handle)
            connected = True
            handle.hw_close()

            return simplejson.dumps(returnDict)

        except Exception as myExc:
            e = sys.exc_info()
            returnDict['failure_message'] = """Exception Occured during register write:\n"""
            returnDict['failure_message'] += '%s\n%s\n%s' % (e[0], traceback.format_exc(e[2]), myExc.message)
            returnDict['failure'] = 1
            connected = False
            handle.hw_close()
            return simplejson.dumps(returnDict)

    @cherrypy.expose
    def execute_function_inprocess(self, function_name, parent_type, parent_name):
        try:
            myFunction = functionByName(function_name.replace("_", " ").encode('ascii', 'ignore'))

            retString = ""
            retString = retString + "<h1> %s </h1>" % myFunction.name

            # First replacement uses **FUNC** replacement, so do it first
            retString = retString + """      
                <p>Execute Function in Progress</p>
                  """

            retString = retString.replace('**FUNC**', myFunction.name.replace("_", " ").encode('ascii', 'ignore'))

            if len(myFunction.inputs) > 0:

                retString = retString + "<h2> Inputs: </h2>"

                retString = retString + '<div style="margin: 0 0 0 50px"> <table>'

                field_index = 0
                for field in myFunction.inputs:
                    if (field.hide == 1):
                        style = """style = "display: none;" """
                    else:
                        style = """style = "display: table-row;" """

                    if (
                            field.translateList == TrueFalse_list or field.translateList == EnabledDisabled_list or field.translateList == OnOff_list):
                        if field.value == 1:
                            retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="checkbox" class="onoffswitch" checked> %s</td></tr>' % (
                            field_index, style, field.name, field_index, field.unit(field))
                        else:
                            retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="checkbox" class="onoffswitch"> %s</td></tr>' % (
                            field_index, style, field.name, field_index, field.unit(field))
                    elif (field.translateList != emptyList):
                        retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                        field_index, style, field.name, field_index, field.translateList[field.value],
                        field.unit(field))
                    else:
                        retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> %s %s</td></tr>' % (
                        field_index, style, field.name, field_index, str(field.translate(field)), field.unit(field))
                    field_index = field_index + 1

                retString = retString + "</table> </div>"

            if hasattr(myFunction, 'assregister'):
                retString = retString + self.access_register(
                    myFunction.assregister.name.replace(" ", "_").encode('ascii', 'ignore'), 'false', 'function',
                    function_name)

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            retString += """<h1>Exception Occured during Host Interface 4cc function execute:</h1>"""
            retString += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            return retString

    @cherrypy.expose
    def execute_function_complete(self, function_name, parent_type, parent_name):
        global connected
        global config

        try:
            myFunction = functionByName(function_name.replace("_", " ").encode('ascii', 'ignore'))
            retval = ""
            retString = ""
            retString = retString + "<h1> %s </h1>" % myFunction.name

            handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                           config.DEVICE_I2C_ADDR)

            retval = myFunction.execute(myFunction, handle)
            connected = True
            handle.hw_close()

            retString = retString + "<p> Function return reports: </p><p> %s </p>" % convtohtml(retval)

            # First replacement uses **FUNC** replacement, so do it first
            retString = retString + "<button onclick=\"javascript:load_hifunction(\'%s\', true, \'none\', \'none\')\">Reload Command Page</button>" % function_name

            retString = retString.replace('**FUNC**', myFunction.name.replace("_", " ").encode('ascii', 'ignore'))

            if len(myFunction.inputs) > 0:

                retString = retString + "<h2> Inputs: </h2>"

                retString = retString + '<div style="margin: 0 0 0 50px"> <table>'

                field_index = 0
                for field in myFunction.inputs:
                    if (field.hide == 1):
                        style = """style = "display: none;" """
                    else:
                        style = """style = "display: table-row;" """

                    if (
                            field.translateList == TrueFalse_list or field.translateList == EnabledDisabled_list or field.translateList == OnOff_list):
                        if field.value == 1:
                            retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="checkbox" class="onoffswitch" checked> %s</td></tr>' % (
                            field_index, style, field.name, field_index, field.unit(field))
                        else:
                            retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="checkbox" class="onoffswitch"> %s</td></tr>' % (
                            field_index, style, field.name, field_index, field.unit(field))
                    elif (field.translateList != emptyList):
                        retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                        field_index, style, field.name, field_index, field.translateList[field.value],
                        field.unit(field))
                    else:
                        retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> %s %s</td></tr>' % (
                        field_index, style, field.name, field_index, str(field.translate(field)), field.unit(field))
                    field_index = field_index + 1

                retString = retString + "</table> </div>"

            if len(myFunction.outputs) > 0:

                retString = retString + "<h2> Outputs: </h2>"
                retString = retString + '<div style="margin: 0 0 0 50px"><table> '

                for field in myFunction.outputs:
                    if (field.hide == 1):
                        style = """style = "display: none;" """
                    else:
                        style = """style = "display: table-row;" """
                    if (field.translateList != emptyList):
                        if field.value < len(field.translateList):
                            retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                            field_index, style, field.name, field_index, field.translate(field), field.unit(field))
                        else:
                            retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                            field_index, style, field.name, field_index, field.value, field.unit(field))

                    else:
                        retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                        field_index, style, field.name, field_index, field.translate(field), field.unit(field))
                    field_index = field_index + 1

                retString = retString + "</table></div>"

            if hasattr(myFunction, 'assregister'):
                retString = retString + self.access_register(
                    myFunction.assregister.name.replace(" ", "_").encode('ascii', 'ignore'), 'true', 'function',
                    function_name)

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            retString += "<h2> Exception Occurred during Host Interface 4cc function execute:</h2>"
            retString += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            connected = False
            handle.hw_close()
            return retString

    @cherrypy.expose
    def access_function_preview(self, function_name, read, parent_type, parent_name):
        try:
            myFunction = functionByName(function_name.replace("_", " ").encode('ascii', 'ignore'))

            retString = ""
            retString = retString + "<h1> %s </h1>" % myFunction.name

            # First replacement uses **FUNC** replacement, so do it first
            retString = retString + """      
                <button onclick="Javascript:jsExecHandler(\'**FUNC**\', \'none\', \'none\')">Execute Function</button>
                  """

            retString = retString.replace('**FUNC**', myFunction.name.replace("_", " ").encode('ascii', 'ignore'))

            if len(myFunction.inputs) > 0:

                retString = retString + "<h2> Inputs: </h2>"

                retString = retString + '<div style="margin: 0 0 0 50px"> <table>'

                field_index = 0
                for field in myFunction.inputs:
                    if (field.hide == 1):
                        style = """style = "display: none;" """
                    else:
                        style = """style = "display: table-row;" """

                    if (
                            field.translateList == TrueFalse_list or field.translateList == EnabledDisabled_list or field.translateList == OnOff_list):
                        if field.value == 1:
                            retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="checkbox" class="onoffswitch" checked onchange="jsFuncChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> %s</td></tr>' % (
                            field_index, style, field.name, field_index, str(function_name), field_index, parent_type,
                            parent_name, field.unit(field))
                        else:
                            retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="checkbox" class="onoffswitch" onchange="jsFuncChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> %s</td></tr>' % (
                            field_index, style, field.name, field_index, str(function_name), field_index, parent_type,
                            parent_name, field.unit(field))
                    elif (field.translateList != emptyList):
                        retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                        field_index, style, field.name, field_index,
                        makeFuncSelect(field.translateList, str(function_name), field_index, field.value, parent_type,
                                       parent_name), field.unit(field))
                    else:
                        retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="text" value="%s" size="%d" onchange="jsFuncChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> %s</td></tr>' % (
                        field_index, style, field.name, field_index, str(field.translate(field)),
                        len(str(field.translate(field))) + 2, str(function_name), field_index, parent_type, parent_name,
                        field.unit(field))
                    field_index = field_index + 1

                retString = retString + "</table> </div>"

            if hasattr(myFunction, 'assregister'):
                retString = retString + self.access_register_preview(
                    myFunction.assregister.name.replace(" ", "_").encode('ascii', 'ignore'), 'true', 'function',
                    function_name)

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            retString += "<h2> Exception Occurred during Host Interface 4cc function setup:</h2>"
            retString += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            return retString

    @cherrypy.expose
    def access_function(self, function_name, read, parent_type, parent_name):
        try:
            myFunction = functionByName(function_name.replace("_", " ").encode('ascii', 'ignore'))

            retString = ""
            retString = retString + "<h1> %s </h1>" % myFunction.name

            # First replacement uses **FUNC** replacement, so do it first
            retString = retString + """      
                <button onclick="Javascript:jsExecHandler(\'**FUNC**\', \'none\', \'none\')">Execute Function</button>
                  """

            retString = retString.replace('**FUNC**', myFunction.name.replace("_", " ").encode('ascii', 'ignore'))

            if len(myFunction.inputs) > 0:

                retString = retString + "<h2> Inputs: </h2>"

                retString = retString + '<div style="margin: 0 0 0 50px"> <table>'

                field_index = 0
                for field in myFunction.inputs:
                    if (field.hide == 1):
                        style = """style = "display: none;" """
                    else:
                        style = """style = "display: table-row;" """

                    if (
                            field.translateList == TrueFalse_list or field.translateList == EnabledDisabled_list or field.translateList == OnOff_list):
                        if field.value == 1:
                            retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="checkbox" class="onoffswitch" checked onchange="jsFuncChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> %s</td></tr>' % (
                            field_index, style, field.name, field_index, str(function_name), field_index, parent_type,
                            parent_name, field.unit(field))
                        else:
                            retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="checkbox" class="onoffswitch" onchange="jsFuncChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> %s</td></tr>' % (
                            field_index, style, field.name, field_index, str(function_name), field_index, parent_type,
                            parent_name, field.unit(field))
                    elif (field.translateList != emptyList):
                        retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                        field_index, style, field.name, field_index,
                        makeFuncSelect(field.translateList, str(function_name), field_index, field.value, parent_type,
                                       parent_name), field.unit(field))
                    else:
                        retString = retString + '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="text" value="%s" size="%d" onchange="jsFuncChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> %s</td></tr>' % (
                        field_index, style, field.name, field_index, str(field.translate(field)),
                        len(str(field.translate(field))) + 2, str(function_name), field_index, parent_type, parent_name,
                        field.unit(field))
                    field_index = field_index + 1

                retString = retString + "</table> </div>"

            if hasattr(myFunction, 'assregister'):
                retString = retString + self.access_register(
                    myFunction.assregister.name.replace(" ", "_").encode('ascii', 'ignore'), 'true', 'function',
                    function_name)

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            retString += "<h2> Exception Occurred during Host Interface 4cc function setup:</h2>"
            retString += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            return retString

    # parent is used when register is displayed as a child on another page, such as
    #     a function page.  This links the write and re-read buttons to the parent
    @cherrypy.expose
    def access_register_preview(self, register, read, parent_type, parent_name):
        global REGS_LIST
        global connected

        try:

            myRegister = registerByName(register.replace("_", " ").encode('ascii', 'ignore'))

            retString = '        <div> <h2 style="margin-left: 0px; padding-left: 0px;"> %s (0x%x) </h2> </div> ' % (
            myRegister.name, myRegister.addr)

            retString += '        <button onclick="Javascript: jsReadHandler(\'%s\' , \'%s\', \'%s\')">Re-read Register</button>' % (
            register, parent_type, parent_name)

            if myRegister.RW != 'RO':
                retString += '            <button onclick="Javascript:jsWriteHandler(\'%s\', \'%s\', \'%s\')">Write Register</button> ' % (
                register, parent_type, parent_name)

            retString += '        <button onclick="Javascript: clearStatusHandler()">Clear Status</button>'

            retString += """        <hr size='1px' color="#aaaaaa" noshade>"""
            retString += """        <div style="display: inline">Status:</div> <div id="regaccessstatus" style="display: inline">Register Read In Progress</div>"""
            retString += """        <hr size='1px' color="#aaaaaa" noshade>"""

            # make an array of html strings to describe the register fields
            sFieldArray = []
            field_index = 0

            sFieldArray.append('<table>')

            for field in myRegister.fields:
                if ((field.name != 'Reserved') and (field.name != 'reserved')):
                    if (field.hide(field) == 1):
                        style = """style = "display: none;" """
                    else:
                        style = """style = "display: table-row;" """

                    sFieldArray.append(
                        '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                        field_index, style, field.name, field_index, "loading", field.unit(field)))
                # update field index even if reserved for easier translation when updating
                field_index += 1

            sFieldArray.append('</table>')

            sFieldInsert = "".join(sFieldArray)

            retString += sFieldInsert

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            exceptMessage = """<div id="regaccessstatus" style="display: inline">Register Read FAILURE:</div>"""
            exceptMessage += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            retString = retString.replace(
                """<div id="regaccessstatus" style="display: inline">Register Read In Progress</div>""", exceptMessage)
            connected = False
            handle.hw_close()
            return retString

    # parent is used when register is displayed as a child on another page, such as
    #     a function page.  This links the write and re-read buttons to the parent
    @cherrypy.expose
    def access_register(self, register, read, parent_type, parent_name):
        global REGS_LIST
        global connected
        global config

        try:

            myRegister = registerByName(register.replace("_", " ").encode('ascii', 'ignore'))

            retString = '        <div> <h2 style="margin-left: 0px; padding-left: 0px;"> %s (0x%x) </h2> </div> ' % (
            myRegister.name, myRegister.addr)

            retString += '        <button onclick="Javascript: jsReadHandler(\'%s\' , \'%s\', \'%s\')">Re-read Register</button>' % (
            register, parent_type, parent_name)

            if myRegister.RW != 'RO':
                retString += '            <button onclick="Javascript:jsWriteHandler(\'%s\', \'%s\', \'%s\')">Write Register</button> ' % (
                register, parent_type, parent_name)

            retString += '        <button onclick="Javascript:clearStatusHandler()">Clear Status</button>'

            retString += """        <hr size='1px' color="#aaaaaa" noshade>"""
            retString += """        <div style="display: inline">Status:</div> ***STATUS***"""
            retString += """        <hr size='1px' color="#aaaaaa" noshade>"""

            if read == 'true':
                handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                               config.DEVICE_I2C_ADDR)

                myRegister.read(handle)
                connected = True
                handle.hw_close()

            # make an array of html strings to describe the register fields
            sFieldArray = []
            field_index = 0

            sFieldArray.append('<table>')

            if myRegister.RW == 'RO':
                for field in myRegister.fields:
                    if ((field.name != 'Reserved') and (field.name != 'reserved')):
                        if (field.hide(field) == 1):
                            style = """style = "display: none;" """
                        else:
                            style = """style = "display: table-row;" """
                        if (field.translateList != emptyList):
                            if field.value < len(field.translateList):
                                sFieldArray.append(
                                    '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                                    field_index, style, field.name, field_index, field.translate(field),
                                    field.unit(field)))
                            else:
                                sFieldArray.append(
                                    '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                                    field_index, style, field.name, field_index, field.value, field.unit(field)))

                        else:
                            sFieldArray.append(
                                '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                                field_index, style, field.name, field_index, field.translate(field), field.unit(field)))
                    # update field index even if reserved for easier translation when updating
                    field_index += 1

            else:
                # No WO at this time, so assume RW
                for field in myRegister.fields:
                    if ((field.name != 'Reserved') and (field.name != 'reserved')):
                        if (field.hide(field) == 1):
                            style = """style = "display: none;" """
                        else:
                            style = """style = "display: table-row;" """

                        if (
                                field.translateList == TrueFalse_list or field.translateList == EnabledDisabled_list or field.translateList == OnOff_list):
                            if field.value == 1:
                                sFieldArray.append(
                                    '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="checkbox" class="onoffswitch" checked onchange="jsOnChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> %s</td></tr>' % (
                                    field_index, style, field.name, field_index, str(register), field_index,
                                    parent_type, parent_name, field.unit(field)))
                            else:
                                sFieldArray.append(
                                    '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="checkbox" class="onoffswitch" onchange="jsOnChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> %s</td></tr>' % (
                                    field_index, style, field.name, field_index, str(register), field_index,
                                    parent_type, parent_name, field.unit(field)))
                        elif (field.translateList != emptyList):
                            sFieldArray.append(
                                '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right">%s %s</td></tr>' % (
                                field_index, style, field.name, field_index,
                                makeSelect(field.translateList, str(register), field_index, field.value, parent_type,
                                           parent_name), field.unit(field)))
                        else:
                            sFieldArray.append(
                                '<tr id="row_%d" %s><td>%s</td><td></td> <td id="field_%d" align="right"> <input type="text" value="%s" size="%d" onchange="jsOnChangeHandler(this, \'%s\', \'%d\', \'%s\', \'%s\')"> %s</td></tr>' % (
                                field_index, style, field.name, field_index, str(field.translate(field)),
                                len(str(field.translate(field))) + 2, str(register), field_index, parent_type,
                                parent_name, field.unit(field)))
                    # update field index even if reserved for easier translation when updating
                    field_index += 1

            sFieldArray.append('</table>')

            sFieldInsert = "".join(sFieldArray)

            retString += sFieldInsert

            retString = retString.replace("""***STATUS***""",
                                          """<div id="regaccessstatus" style="display: inline">Register Read SUCCESS</div>""")

            return retString

        except Exception as myExc:
            e = sys.exc_info()
            exceptMessage = """<div id="regaccessstatus" style="display: inline">Exception Occurred During Register Read:<br>"""
            exceptMessage += convtohtml(
                '%s\n%s\n%s' % (escape_html(e[0]), escape_html(traceback.format_exc(e[2])), myExc.message))
            exceptMessage += """</div>"""
            retString = retString.replace("""***STATUS***""", exceptMessage)
            connected = False
            handle.hw_close()
            return retString


if __name__ == '__main__':
    if len(sys.argv) > 1 :
        port = int(sys.argv[1])
    else :
        port = 8080
    port = 1313 # enzo add
    print(port)
    cherrypy.config.update({'server.socket_host': '127.0.0.1',
                            'server.socket_port': port, })

    conf = {'/html': {'tools.staticdir.on': True,
        'tools.staticdir.dir': '%s/html' %file_path},
            '/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': '%s/css' %file_path},
            '/resources': {'tools.staticdir.on': True,
        'tools.staticdir.dir': '%s/resources' %file_path},
            '/docs': {'tools.staticdir.on': True,
        'tools.staticdir.dir': '%s/docs' %file_path}}
    
    cherrypy.quickstart(StringGenerator(), '/', config=conf)
    
