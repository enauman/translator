# translator
<img src="20230910_131031.GIF" width="600">
<h3>Transcribes speech to text then translates to 4 different languages for 3 daisy-chained 16x32 rgb matrix displays</h3>
<h4>BOM</h4>
<ul>
  <li><a href="https://www.adafruit.com/product/420">3 x Medium 16x32 RGB LED matrix panel - 6mm Pitch</a>. Each comes with 16-pin ribbon cable and power cables (matrix is powered separate from Raspberry Pi) but not a power adapter. </li>
  <li><a href="https://www.adafruit.com/product/276">5v 2amp power adapter</a>. You will have to hack a connection to the power cables. I cut the barrel plug off one and soldered the leads to the power cables.
  <li><a href="https://www.adafruit.com/product/4295">Raspberry Pi 4 Model B - 1 GB RAM</a> (other models can work as documented on <a href="https://github.com/hzeller/rpi-rgb-led-matrix">hzeller Raspberry Pi/matrix library</a>, this is the one I'm using)</li>
  <li><a href="https://www.adafruit.com/product/4298">Raspberry Pi power supply</a>
  <li>If you can make a 2-sided pcb get this <a href="https://www.adafruit.com/product/1988">40-pin ribbon cable</a>, if not get the <a href="https://www.adafruit.com/product/1989">T-cobbler breakout</a> to connect the Pi to the matrix with some jumper wires and a breadboard.</li>
  <li><a href="https://www.adafruit.com/product/3658">M2.5 nylon screws to attach the Pi to the 3d printed bracket if you want to secure it (see below)</a></li>
  <li>Fair to good quality <a href="https://www.microcenter.com/product/645865/fifine-usb-microphone-%e2%80%93-k650">USB mic</a>, this works for me, where a <a href="https://www.adafruit.com/product/3367">very cheap one</a> didn't work well enough for speech recognition and was too close to the Rasperry Pi fan.</li>
  <li><a href="https://www.adafruit.com/product/848">10mm rgb led, common anode</a> to show current display color</li>
  <li><a href="https://www.adafruit.com/product/1010">12mm tactile button</a> to select display color</li>
  <li><a href="https://www.amazon.com/Phillips-Countersunk-Machine-Screws-100pcs/dp/B018RSV7GM/ref=sr_1_6?crid=1DPNAOIWURN82&keywords=m4+machine+screw+6mm&qid=1694360762&sprefix=m4+machine+screw+6mm%2Caps%2C96&sr=8-6">M4 6mm machine screws</a> to attach the matrix to 3d printed frame parts (see below)</li>
  <li><a href="https://www.amazon.com/uxcell-Position-Panel-Switch-Latching/dp/B01N11OG51/ref=sr_1_4?crid=MVILGR469TU7&keywords=4+throw+slide+switch&qid=1694359070&sprefix=4+throw+slide+switch%2Caps%2C98&sr=8-4">4-pole slide switch</a>, something like this if you want settings for multiple language translations. I hacked one off an old clock radio.</li>
  <li><a href="https://www.adafruit.com/product/1443">latching push button</a>, to start and stop voice/translation service; something like this, I hacked one off something</li>
</ul>
<h4>Fabricated Parts</h4>
<ul>
  <li><a href="https://www.tinkercad.com/things/iSzlixS7yKj-matrix-frame">3D printed frames/brackets</a></li>
  <li><a href="https://oshwlab.com/enauman/rgb-panel">Easy EDA project with 2 pcb designs.</a> Single-sided pcb is to attach 10mm rgb led and 12mm button for showing and choosing color of display. 2-sided pcb is to attach 16-pin ribbon cable from matrix display to 40-pin ribbon cable going to Raspberry Pi, as well as connecting rgb led + button, latching control button to start/stop voice/translation service, and 4-pole slide switch for selecting each of 4 languages.</li>
</ul>
<h4>Software, Dependencies</h4>
<ul>
<li>Raspberry Pi OS Lite (64-bit), translate-shell errors on 32-bit</li>
<li>Raspberry Pi account name I used is "translator" and is hard coded in program files main.py and voice_service.py (see file path below)</li>
<li>Create project directory named "app" on Pi and add files from this git project.</li>
<li><a href="https://pypi.org/project/SpeechRecognition/">Speech Recognition</a> library with dependencies in documentation</li>
<li><a href="https://lindevs.com/install-translate-shell-on-raspberry-pi/">Translate-shell</a>, I think this is what I followed to get it on Raspberry Pi</li>
<li><a href="https://github.com/hzeller/rpi-rgb-led-matrix/tree/master">hzeller rpi-rgb-led-matrix library</a>, build and put in same folder as application</li>
</ul>
<h4>Tips and Configurations</h4>
<ul>
<li>If using non-Latin language characters, create bdf font files by downloading and converting them with <a href="https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/use-otf2bdf">otf2bdf</a> on Linux (easiest), put the bdf file in the rpi-rgb-led-matrix library font folder.</li>
<li><a href="https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/updating-alsa-config">Tip for configuring USB mic</a> to work as default recording device.</li>
<li><a href="https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup#method-3-systemd">Autorun program on startup</a>. I used systemcd approach with the following in my Unit File:<br />
  <pre>
    <code>
[Unit]
Description=Run translation service
After=multi-user.target

[Service]
ExecStart=/usr/bin/python -u /home/translator/app/main.py
StandardOutput=file:/home/translator/app/translator.log
StandardError=inherit

[Install]
WantedBy=multi-user.target
    </code>
  </pre>
  </li>
  <li>Because of autorun, root needs access to program files so file names are written with full path included. Also files need rwx permissions added for "all". That's the only way I could get everything to work from autorun.</li>
  </ul>

