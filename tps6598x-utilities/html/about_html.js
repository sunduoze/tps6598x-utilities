var obAboutHtml =
'<div> \
<p>         TPS6598x Host Utilities GUI Version 2.3  </p> \
</div> \
<div> \
<table style="width: 100%;text-align: center;padding: 1px; font-size: 18px"> \
    <tr style="background-color: #cccccc;"> \
        <td style="width: 25%" font="Arial !important"> \
        Version \
        </td> \
        <td style="width: 75%"> \
        Change List Description \
        </td> \
    </tr> \
    <tr> \
        <td> \
        1.0 September, 2015\
        </td> \
        <td style="text-align: left"> \
        <ul>\
            <li>Initial Release of TPS65982 debugging scripts. Supports Aardvark USB to I2C adapter and text-based scripts.</li>\
        </ul>\
        </td> \
    </tr> \
    <tr> \
        <td> \
        2.0 March, 2016\
        </td> \
        <td style="text-align: left"> \
        <ul>\
            <li>Expanded upon python debugging scripts to provide a GUI interface (gui.py in source directory.) Added support for FTDI-based USB-to-Many debugging interface and USB2.0 Endpoint access to the host interface (requires firmware version 1.7.4 or later.)</li>\
        </ul>\
        </td> \
    </tr> \
    <tr> \
        <td> \
        2.1 April, 2016\
        </td> \
        <td style="text-align: left"> \
        <ul>\
            <li>Minor Updates. Added read, write and ADCs commands. Fixed a bug that made header scroll with content.</li>\
        </ul>\
        </td> \
    </tr> \
    <tr> \
        <td> \
        2.2 May, 2016\
        </td> \
        <td style="text-align: left"> \
        <ul>\
            <li>Added VDMs Command.</li>\
        </ul>\
        </td> \
    </tr> \
    <tr> \
        <td> \
        2.3 July, 2016\
        </td> \
        <td style="text-align: left"> \
        <ul>\
            <li>Minor Updates. Fixed a bug that did not change I2C address when it is changed in config. Added new registers: User VID Config, User VID Status, User SVID Rx Attn, User SVID Rx non-Attn </li>\
        </ul>\
        </td> \
    </tr> \
    <tr> \
        <td> \
        2.4 August, 2016\
        </td> \
        <td style="text-align: left"> \
        <ul>\
            <li>Fixed a bug that would not talk correctly to a device that is in sleep mode</li>\
            <li>Added exception trace output to any exceptions thrown in GUI to help handle reported issues. Users should screen capture exception trace when reporting an issue.</li>\
        </ul>\
        </td> \
    </tr> \
</table><br> \
<p>Support Information: To report a bug or to request any further assistance on this tool, please post your comment or question in the following E2E Forum Room: <a href="http://www.ti.com/usbforum">E2E USB Forum</a></p> \
<p> \
<strong>DISCLAIMER:</strong><br><br> \
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" \
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, \
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR \
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR \
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, \
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, \
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; \
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, \
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR \
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, \
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.<br> \
</p> \
 \
</div>';