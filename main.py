#!/usr/bin/python

import sys
import getopt

import alsa_hw_data
import config_writer
from pcm_holder import pcm_holder
from UI import UI

alsa_hw_data.list_cards()

interface = UI()
pcms=[]

def gen_fun():
	i=interface.query_listbox()
	if i == -1:
		interface.make_confirm_diag("No device selected! Aborting.")
		return
	dmix=interface.dmix.get()
	mult=interface.multi.get()

	rate=interface.rate_box.get()
	period_time=interface.p_time_box.get()
	period_size=interface.p_size_box.get()
	buffer_size=interface.b_size_box.get()

	if dmix == True and mult == False:
		dmixer = pcm_holder("dmixer", "dmix", "hw:"+str(i), rate, period_time, period_size, buffer_size)
		pcms.append(dmixer)
	elif mult == True:
		snd = pcm_holder("snd_card", "hw", "hw:"+str(i), rate, period_time, period_size, buffer_size)
		pcms.append(snd)

		default = pcm_holder("!default", "asym", "out", rate, period_time, period_size, buffer_size)
		pcms.append(default)


	else:
		default = pcm_holder("!default", "hw", "hw:"+str(i), rate, period_time, period_size, buffer_size)
		pcms.append(default)

	config_writer.write_pcm(pcms)
	interface.make_confirm_diag("Operation completed!")

interface.make_buttons(gen_fun)
interface.make_listbox(alsa_hw_data.cards)
interface.make_checkbuttons()
interface.make_spinboxes()

interface.run_loop()
