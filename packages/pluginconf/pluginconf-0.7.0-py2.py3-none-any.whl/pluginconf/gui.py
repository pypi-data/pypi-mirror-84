# encoding: UTF-8
# api: python
# type: ui
# category: io
# title: Config GUI
# description: Display plugins + options in setup window
# version: 0.3
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
# Very crude, and not as many options as the Gtk/st2 implementation.
#


import PySimpleGUI as sg
import pluginconf
import glob, json, os, re


# temporarily store collected plugin meta data and config: details
plugins = {}
options = {}


#-- show configuation window
#
# · updates config{} settings and plugin_states{} on saving
#
def window(config={}, plugin_states={}, files=["*/*.py"], **kwargs):

    plugins = read_options(files)
    layout = plugin_layout(plugins.values(), config, plugin_states)
    #print(repr(layout))
    
    # pack window
    layout = [
        [sg.Column(layout, size=(560,620), scrollable=True)],
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
        print(plg.get("id"))
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
                  font="bold", pad=(0,(5,0))
             ),
             sg.Text("{}.{}".format(e.get("type"), e.get("category")), text_color="#333"),
             sg.Text(e.get("version"), text_color="#ec7")
         ],
         [
             sg.Text(e.get("description", ""), tooltip=e.get("doc"), font=("sans", 8), pad=(32,8))
         ]
    ]

# widgets for single config option
def option_entry(o, config):
    print(o)
    name = o.get("name", "")
    desc = o.get("description", name)
    type = o.get("type", "text")
    options[name] = o
    val = config.get(name, o.get("default", o.get("value", "")))
    if type in ("text", "str", "string"):
        return [
            sg.Text(desc, pad=(50,2), tooltip=name),
            sg.InputText(key=name, default_text=str(val), size=(20,1))
        ]
    elif type in ("bool", "boolean", "checkbox"):
        return [
            sg.Checkbox(desc, key=name, default=cast.bool(val), tooltip=name, pad=(40,2))
        ]
    elif type in ("int", "integer", "number"):
        return [
            sg.Text(desc, pad=(50,2), tooltip=name),
            sg.InputText(key=name, default_text=str(val), size=(6,1))
        ]
    elif type in ("select", "choice", "choice"):
        o["select"] = parse_select(o.get("select", ""))
        values = [v for v in o["select"].values()]
        return [
            sg.Text(desc, pad=(50,2), tooltip=name),
            sg.Combo(key=name, default_value=o["select"].get(val, val), values=values, size=(15,1))
        ]
    # types not implemented here: `table`, `dict`
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
    @staticmethod
    def bool(v):
        if v in ("1", 1, True, "true", "TRUE"):
            return True
        return False
    @staticmethod
    def int(v):        
        return int(v)
    @staticmethod
    def fromtype(v, t, opt):
        if t in ("int","integer","number"):
            return cast.int(v)
        elif t in ("bool","boolean"):
            return cast.bool(v)
        elif t in ("select", "choice"):
            inverse = dict((v,k) for k,v in opt["select"].items())
            return inverse.get(v, v)
        else:
            return v


