# translator
<h3>Transcribes speech to text then translates to 4 different languages for 3 daisy-chained 16x32 rgb matrix displays</h3>
<h4>BOM</h4>
<ul>
  <li><a href="https://www.adafruit.com/product/420">3 x Medium 16x32 RGB LED matrix panel - 6mm Pitch</a>. Each comes with 16-pin ribbon cable and power cables (matrix is powered separate from Raspberry Pi) but not a power adapter. </li>
  <li><a href="https://www.adafruit.com/product/276">5v 2amp power adapter</a>. You will have to hack a connection to the power cables. I cut the barrel plug off one and soldered the leads to the power cables.
  <li><a href="https://www.adafruit.com/product/4295">Raspberry Pi 4 Model B - 1 GB RAM</a> (other models can work as documented on <a href="https://github.com/hzeller/rpi-rgb-led-matrix">hzeller Raspberry Pi/matrix library</a>, this is the one I'm using)</li>
  <li><a href="https://www.adafruit.com/product/4298">Raspberry Pi power supply</a>
  <li>If you can make a 2-sided pcb see below, if not get the <a href="https://www.adafruit.com/product/1989">T-cobbler breakout</a> to connect the Pi to the matrix with some jumper wires and a breadboard.</li>
  <li><a href="https://www.adafruit.com/product/3658">M2.5 nylon screws to attach the Pi to the 3d printed bracket if you want to secure it (see below)</a></li>
  <li>Fair to good quality <a href="https://www.microcenter.com/product/645865/fifine-usb-microphone-%e2%80%93-k650">USB mic</a>, this works for me, where a <a href="https://www.adafruit.com/product/3367">very cheap one</a> didn't work well enough for speech recognition and was too close to the Rasperry Pi fan.</li>
  <li><a href="https://www.adafruit.com/product/848">10mm rgb led, common anode</a></li>
  <li><a href="https://www.adafruit.com/product/1010">12mm tactile button</a></li>
  <li><a href="https://www.amazon.com/uxcell-Position-Panel-Switch-Latching/dp/B01N11OG51/ref=sr_1_4?crid=MVILGR469TU7&keywords=4+throw+slide+switch&qid=1694359070&sprefix=4+throw+slide+switch%2Caps%2C98&sr=8-4">4-pole slide switch</a>, something like this if you want settings for multiple language translations. I hacked one off an old clock radio.</li>
  <li><a href="https://www.adafruit.com/product/1443">latching push button</a>, something like this, I hacked one off something</li>
</ul>
<p>Application requires <a href="https://github.com/hzeller/rpi-rgb-led-matrix">hzeller rpi-rgb-led-matrix</a> library located in same application folder.</p>

<li><a href="https://www.adafruit.com/product/1988">40-pin ribbon cable</a></li>
