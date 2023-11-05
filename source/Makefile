all: supercon_menu interactive

supercon_menu: supercon_menu.py
	mpremote cp $^ :

menudemo: menudemo.py
	mpremote cp $^ :

vectorscope: vectorscope.py
	mpremote cp $^ :

lissajous: lissajous.py
	mpremote cp $^ :

libs: 
	mpremote cp *.py :

bitflip: bit_flip_pio.py
	mpremote reset 
	sleep 1
	mpremote run $^

interactive: RUNME
	mpremote resume

RUNME: vectoros.py
	mpremote reset
	sleep 1
	mpremote run $^

hb9fsi:
	mpremote cp supercon_menu.py :
	mpremote cp vos_launch.py :
	mpremote cp drbokko.py :
	mpremote cp hb9fsi.py :
	mpremote cp hb9fsi_qr.jpg :
	mpremote cp bell202.py :
	mpremote cp vectorscope_mock.py :
	mpremote reset

%.png: %.dot	
	dot  -T png -o $@ < $^
	sxiv $@

.PHONY: RUNME
