# encoding: UTF-8
# api: python
# type: ui
# category: io
# title: Config GUI
# description: Display plugins + options in setup window
# version: 0.4
# depends: python:pysimplegui (>= 4.0)
# priority: optional
# config: -
#
# Creates a PySimpleGUI options list. Scans a given list of *.py files
# for meta data, then populates a config{} dict and (optionally) a state
# map for plugins themselves.
#
#    jsoncfg = {}
#    pluginconf.gui.window(jsoncfg, {}, ["plugins/*.py"])
#
# Very crude, and not as many widgets as the Gtk/St2 implementation.
#


import PySimpleGUI as sg
import pluginconf
import glob, json, os, re


# temporarily store collected plugin meta data and config: details
options = {}
plugins = {
    "global": {
        "id":"pluginconf", "title":"global settings", "version":"0.0",
        "type":"virtual", "category":"ui", "api":"python", "config": [
            {"name":"test", "type":"bool", "value":1, "description":"…"}
        ]
    }
}


#-- show configuation window
#
# · reads *.py files and crafts a settings dialog from meta data
# · updates config{} settings and plugin_states{} on saving
# · if files= is omitted, then plugins`→"global"→config[] should be prepopulated
#
def window(config={}, plugin_states={}, files=["*/*.py"], theme="DefaultNoMoreNagging", **kwargs):
    if theme:
        sg.theme(theme)
    if files:
        plugins = read_options(files)
    layout = plugin_layout(plugins.values(), config, plugin_states)
    #print(repr(layout))
    
    # pack window
    layout = [
        [sg.Column(layout, size=(580,620), scrollable="vertically", element_justification='left')],
        [sg.Button("Save")]
    ]
    win = sg.Window(title="Options", layout=layout, **kwargs)

    # wait for save/exit        
    event,data = win.read()
    if event=="Save":
        print(data)
        for k,v in data.items():
            if options.get(k):
                config[k] = cast.fromtype(data[k], options[k]["type"], options[k])
            elif plugins.get(k):
                plugin_states = v
    #print(config)
    win.close()
    
    
# craft list of widgets for each read plugin
def plugin_layout(ls, config, plugin_states):
    layout = []
    for plg in ls:
        #print(plg.get("id"))
        layout = layout + plugin_entry(plg, plugin_states)
        for opt in plg["config"]:
            layout.append(option_entry(opt, config))
    return layout
    
# checkbox for plugin name
def plugin_entry(e, plugin_states):
    id = e["id"]
    return [
         [
             sg.Checkbox(
                  e.get("title", id), key=id, default=plugin_states.get(id, 0), tooltip=e.get("doc"), metadata="plugin",
                  font="bold", pad=(0,(8,0))
             ),
             sg.Text("({}/{})".format(e.get("type"), e.get("category")), text_color="#005", pad=(0,(8,0))),
             sg.Text(e.get("version"), text_color="#a72", pad=(0,(8,0)))
         ],
         [
             sg.Text(e.get("description", ""), tooltip=e.get("doc"), font=("sans", 10), pad=(26,(0,10)))
         ]
    ]

# widgets for single config option
def option_entry(o, config):
    #print(o)
    name = o.get("name", "")
    desc = o.get("description", name)
    type = cast.map.get(o.get("type", "text"))
    options[name] = o
    val = config.get(name, o.get("value", ""))
    if o.get("hidden"):
        pass
    elif type == "str":
        return [
            sg.InputText(key=name, default_text=str(val), size=(20,1), pad=((50,0),5)),
            sg.Text(desc, pad=(5,2), tooltip=name, justification='left')
        ]
    elif type == "bool":
        return [
            sg.Checkbox(desc, key=name, default=cast.bool(val), tooltip=name, pad=((40,0),2))
        ]
    elif type == "int":
        return [
            sg.InputText(key=name, default_text=str(val), size=(6,1), pad=((50,0),3)),
            sg.Text(desc, pad=(5,2), tooltip=name)
        ]
    elif type == "select":
        o["select"] = parse_select(o.get("select", ""))
        values = [v for v in o["select"].values()]
        return [
            sg.Combo(key=name, default_value=o["select"].get(val, val), values=values, size=(15,1), pad=((50,0),0)),
            sg.Text(desc, pad=(5,2), size=(50,1), tooltip=name)
        ]
    elif type == "dict":  # or "table" rather ?
        print([
            dict(values=config.get(name, ["", ""]), headings=o.get("columns", "Key,Value").split(","), num_rows=5)
        ])
    return []


#-- read files, return dict of {id:pmd} for all plugins
def read_options(files):
    ls = [pluginconf.plugin_meta(fn=fn) for pattern in files for fn in glob.glob(pattern)]
    return dict(
        (meta["id"], meta) for meta in ls
    )

#-- split up `select: a=1|b=2|c=3` or `select: foo|bar|lists`
def parse_select(s):
    if re.search("([=:])", s):
        return dict(re.findall("(\w+)\s*[=:>]+\s*([^=,|:]+)", s))
    else:
        return dict([(v, v) for v in re.findall("\s*([^,|;]+)\s*", s)])


#-- map option types (from strings)
class cast:
    map = dict(
        text="str", str="str", string="str",
        bool="bool", boolean="bool", checkbox="bool", 
        int="int", integer="int", number="int",
        select="select", choice="select", options="select",
        table="dict", array="dict", dict="dict"
    )
    map["list"] = "dict"
    @staticmethod
    def bool(v):
        if v in ("1", 1, True, "true", "TRUE", "yes", "YES", "on", "ON"):
            return True
        return False
    @staticmethod
    def int(v):        
        return int(v)
    @staticmethod
    def fromtype(v, t, opt):
        if t == "int":
            return cast.int(v)
        elif t == "bool":
            return cast.bool(v)
        elif t == "select":
            inverse = dict((v,k) for k,v in opt["select"].items())
            return inverse.get(v, v)
        else:
            return v


