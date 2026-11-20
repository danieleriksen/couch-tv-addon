# couch-tv bridge add-on for Home Assistant

Runs the couch-tv bridge (https://github.com/Seagey/couch-tv, option B) on Home Assistant OS, for a
Samsung TV. Untested community wrapper: not part of couch-tv.

Options: `tv_ip` (the TV's address), `tv_name`, `bridge_ip` (leave empty: found by itself),
`country`, `open_on_power_on`, `pairing_key` (empty = no password on the phone remote).

After it starts:
- Phone remote: http://<home assistant address>:5400
- Samsung app built for this bridge: http://<home assistant address>:5400/CouchTV.wgt
  Put it in place of CouchTV.wgt in the unzipped couch-tv-samsung-setup folder, then run the installer.

Settings and the TV's pairing token are kept in the add-on's /data. Uninstalling the add-on removes them.
