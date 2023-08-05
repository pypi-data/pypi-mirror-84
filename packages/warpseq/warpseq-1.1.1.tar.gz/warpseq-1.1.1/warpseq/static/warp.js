const SWITCHER_DIV = 'nav1'
const NAV_DIV = 'nav2';
const WORKSPACE_DIV = 'workspace';

const SONG = 'song';
const DEVICE = 'device';
const INSTRUMENT = 'instrument';
const SCALE = 'scale';
const SCENE = 'scene';
const TRACK = 'track';
const PATTERN = 'pattern';
const TRANSFORM = 'transform';
const DATA_POOL = 'data_pool';
const GRID = 'grid';
const CLIP = 'clip';

const OBJECT_CATEGORIES = [ 'clips', 'scenes', 'data_pools', 'tracks', 'devices', 'instruments', 'patterns', 'scales', 'transforms' ]

var playing_objects = {
    'clips' : [],
    'tracks' : [],
    'devices' : [],
    'instruments' : [],
    'patterns' : [],
    'scales' : [],
    'transforms' : [],
    'scenes' : [],
    'data_pools' : [],
}

/**********************************************************************************************************************/
/* general  utilities                                                                                                 */
/**********************************************************************************************************************/

function model_post(data, on_success, on_failure) {
    in_data = JSON.stringify(data);
    if (data['cmd'] != 'status_report') {
        console.log("model_post")
        console.log(data)
    }
    if (on_success == null) {
        on_success = function(data) {}
    }
    if (on_failure == null) {
        on_failure = function(data) {}
    }
    $.ajax({
        type: 'POST',
        url: '/model',
        data: in_data,
        dataType: 'json',
        contentType: "application/json",
        cache: false,
        success: function(data_out) {
            if (data['cmd'] != 'status_report') {
                console.log(data_out);
            }
            on_success(data_out)
        },
        error: function(data_out) {
            if (data['cmd'] != 'status_report') {
                alert("Error");
            }
            console.log("ERROR: " + data_out);
            console.log(data_out);
            on_failure(data_out);
        }
    });

}

function load_into_div(url, div, cb) {
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'text',
        cache: false,
        success: function(data) {
            $("#" + div).html(data);
            if (cb != null) {
                cb();
            }
        },
        error: function(data) {
            //console.log(data);
            try {
                flash_error(data.responseJSON['msg']);
            } catch(err) {
                console.log(err);
                console.log("communication with server failed");
            }
        }
    });
}

function model_delete(category, item) {
   if (item == null) {
       item = document.getElementById("obj_id").value;
   }
   var r = confirm("Confirm Deletion?");
   if (r == false) {
      return;
   }
   model_post({ "cmd" : "delete_" + category, "id" : item }, function(data) {
      load_into_nav(category);
      close_workspace();
   });
}

function model_copy(category, item) {
   if (item == null) {
       item = document.getElementById("obj_id").value;
   }
   model_post({ "cmd" : "copy_" + category, "id" : item }, function(data) {
         load_into_nav(category);
   });
}

function model_do_edit(category, textboxes=[], selects=[], multiple_selects=[], toggles=[], ranges=[], cb=null) {
   if (cb == null) {
       cb = function(data) {}
   }
   var data = {};
   var key = "";
   if (category != 'song') {
      data["id"] = document.getElementById("obj_id").value;
   }
   for(i=0; i<textboxes.length; i++) {
       key = textboxes[i];
       value = document.getElementById(key).value;
       data[key] = value;
   }
   for(i=0; i<selects.length; i++) {
       key = selects[i];
       value = null_if_dash(select2_get_selection(key));
       data[key] = value;
   }
   for(i=0; i<multiple_selects.length; i++) {
       key = multiple_selects[i];
       value = null_if_empty(select2_get_selections(key));
       data[key] = value;
   }
   for(i=0; i<toggles.length; i++) {
       key = toggles[i];
       value = document.getElementById(key).checked;
       data[key] = value;
   }
   console.log(data);
   for(i=0; i<ranges.length; i++) {
       key = ranges[i];
       value = document.getElementById(key).value;
       data[key] = value;
   }
   model_post({
       "cmd" : "edit_" + category,
       "data" : data
   }, cb);
}

function model_do_new(category) {

    model_post({
        "cmd" : "new_" + category,
        "data" : {}
    }, function(data) {
        //console.log(data)
        load_into_nav(category);
        load_into_workspace(category, data.data);
    });
}

function default_cell_renderer(entry) {
   return entry['value'];
}

function generic_grid_init(cmd, category, grid_name="myGrid", reload=null, override_renderer=null) {

   var obj_id = document.getElementById("obj_id").value;
   model_post({
       "cmd" : cmd,
       "id" : obj_id,
       "data" : { "category" : category }
   }, function(data) {

       var chosen_renderer = default_cell_renderer;
       if (override_renderer != null) {
           chosen_renderer = override_renderer;
       }

       var columnDefs = data["data"]["column_defs"];

       for(i=0; i<columnDefs.length; i++) {
           columnDefs[i]["cellRenderer"] = chosen_renderer;
       }

       var rowData = data["data"]["row_data"];
       var gridDiv = document.querySelector('#' + grid_name);

       columnDefs[0]["rowDrag"] = function(params) {
           return !params.node.group;
       };

       gridDiv.innerHTML = '';

       var gridOptions = {
           columnDefs: columnDefs,
           rowData: rowData,
           singleClickEdit: true,
           stopEditingWhenGridLosesFocus: true,
           rowDragManaged: true,
           enableMultiRowDragging: true,
           rowSelection: 'multiple',
           rowDeselection: true,
           animateRows: true,
           onGridReady: (params) => {
               gridOptions.api.sizeColumnsToFit();
           },
           onCellEditingStopped: function(event) { update_grid_backend(cmd, category, gridOptions, reload); },
           onCellValueChanged: function(event) { update_grid_backend(cmd, category, gridOptions, reload); },
           onRowDragEnd: function(event) { update_grid_backend(cmd, category, gridOptions, reload); },
       };

       new agGrid.Grid(gridDiv, gridOptions);

       $('#new_row_button').on('click', function() {
           gridOptions.api.applyTransaction({ add: [{}] });
       });
       $('#new_row4_button').on('click', function() {
           for(i=0; i<4; i++) {
               gridOptions.api.applyTransaction({ add: [{}] });
           }
       });
       $('#new_row8_button').on('click', function() {
           for(i=0; i<8; i++) {
               gridOptions.api.applyTransaction({ add: [{}] });
           }
       });

       $('#delete_row_button').on('click', function() {
           items = []
           var nodes = gridOptions.api.getSelectedNodes();
           for(i=0; i<nodes.length; i++) {
              items.push(nodes[i]["childIndex"]);
           }
           delete_grid_nodes(cmd, items);
           var selected = gridOptions.api.getSelectedNodes();
           var selected2 = [];
           for (j=0; j<selected.length; j++) {
               selected2.push(selected[j].data);
           }
           gridOptions.api.applyTransaction({ remove: selected2 });
       });

   });
}

/**********************************************************************************************************************/
/* page specifics                                                                                                     */
/**********************************************************************************************************************/

function clear_slots() {
   $('#slots').val(null).trigger('change');
}

/**********************************************************************************************************************/
/* populates the first nav widget dynamically                                                                         */
/**********************************************************************************************************************/

function load_into_switcher() {
   load_into_div("/pages/switcher/1", SWITCHER_DIV);
}

/**********************************************************************************************************************/
/* clicking on the first nav menu loads something into the second nav menu                                            */
/**********************************************************************************************************************/

function clear_nav() {
    $("#" + NAV_DIV).html('');
}

function load_into_nav(category) {

    var current_category = document.getElementById("current_category");
    if (current_category) {
       current_category = current_category.value;
    }

    function light_up() {
        // TODO: make category in datastructures use the non-plural version to eliminate this
        var cat = category + "s";
        console.log("CATEGORY=" + cat);
        if (category != 'song') {
            toggle_lights(playing_objects, [cat], true);
        }
    }

    load_into_div("/pages/" + category + "/list", NAV_DIV, light_up);
}

/**********************************************************************************************************************/
/* clicking on the second nav menu loads something into the workspace                                                 */
/**********************************************************************************************************************/

function load_into_workspace(category, item) {
    toggle_nav2(item);
    load_into_div("/pages/" + category + "/" + item, WORKSPACE_DIV);
}

function toggle_nav2(item) {
    $(".nav2_item").removeClass("nav2_item_active");
    $("#nav2_item_" + item).addClass("nav2_item_active");
}

function toggle_switcher(category) {
    $(".switcher_category").removeClass("switcher_item_active");
    $(".switcher_category").addClass("switcher_item_inactive");
    $("#" + category).removeClass("switcher_item_inactive");
    $("#" + category).addClass("switcher_item_active");
}

/**********************************************************************************************************************/
/* first nav menu                                                                                                     */
/**********************************************************************************************************************/

function load_song()        {   toggle_switcher('song_category'); clear_nav(); load_into_workspace(SONG, 0, 0) }
function load_instruments() {   toggle_switcher('instrument_category'); load_into_nav(INSTRUMENT);       }
function load_devices()     {   toggle_switcher('device_category'); load_into_nav(DEVICE);           }
function load_scales()      {   toggle_switcher('scale_category'); load_into_nav(SCALE);            }
function load_scenes()      {   toggle_switcher('scene_category'); load_into_nav(SCENE);            }
function load_tracks()      {   toggle_switcher('track_category'); load_into_nav(TRACK);            }
function load_patterns()    {   toggle_switcher('pattern_category'); load_into_nav(PATTERN);          }
function load_transforms()  {   toggle_switcher('transform_category'); load_into_nav(TRANSFORM);        }
function load_data_pools()  {   toggle_switcher('data_pool_category'); load_into_nav(DATA_POOL);        }

/**********************************************************************************************************************/
/* startup page                                                                                                       */
/**********************************************************************************************************************/

function load_initial_ui_state(data) {
    load_into_switcher();
    load_into_nav(SONG);
    load_song();
}

/**********************************************************************************************************************/
/* WORKSPACE DIALOGS                                                                                                  */
/**********************************************************************************************************************/

function select2_get_selection(element) {
    data = $("#"+element).select2('data');
    for(var index in data) {
        if (data[index].selected) {
            console.log("select2_get_selection => " + data[index].text)
            return data[index].text;
        }
    }
    return null;
}

function select2_get_selections(element) {
    var results = [];
    data = $("#"+element).select2('data')
    for(var index in data) {
        if (data[index].selected) {
            results.push(data[index].text);
        }
    }
    return results;
}

function select2_activate(field) {
    var element = $("#" + field)
    element.select2({
        width: 200
    });
    element.on('select2:select', function (e) {
        if (intercept_field(field, select2_get_selection(field))) {
           edit_this();
        }
    });
}

function textbox_activate(field) {
    $("#" + field).focusout(function(){
         if (intercept_field(field, $("#" + field).value)) { edit_this(); }
    });
    document.getElementById(field).addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
            if (intercept_field(field, $("#" + field).value)) { edit_this(); }
        }
    });
}

function range_activate(field) {
  var elem = $("#" + field);
  document.getElementById(field).addEventListener("input", () => {
      $("#" + field + "_value").text(elem[0].value);
      edit_this();
  });
}

function toggle_activate(field) {
    document.getElementById(field).addEventListener('change', (event) => {
        edit_this();
    });
}

function null_if_dash(item) {
   if (item == "-") {
      return null;
   }
   return item;
}

function null_if_empty(alist) {
   if (alist.length == 0) {
       return null;
   }
   return alist
}

function close_workspace() {
   $("#" + WORKSPACE_DIV).html('');
}

/**********************************************************************************************************************/
/* FLASH MESSAGES                                                                                                     */
/**********************************************************************************************************************/

function flash_error(msg) {
   //console.log("error: " + msg);
   //$("#flash").removeClass("flash_happy");
   //$("#flash").addClass("flash_error");
   //$("#flash").html(msg);
}


/**********************************************************************************************************************/

function stop() {
    model_post({
       "cmd" : "stop"
   }, null);
}

function play() {
    model_post({
       "cmd" : "play"
   }, null);
}

function midi_panic() {
    model_post({
       "cmd" : "midi_panic"
   }, null);
}

/**********************************************************************************************************************/
/* SONG                                                                                                               */
/**********************************************************************************************************************/

function edit_song(cb = null) {
    model_do_edit("song",
        textboxes=["new_name", "filename"],
        selects=["scale"],
        multiple_selects=[],
        toggles=[],
        ranges=["tempo"],
    );
}

function file_new() {
    if (confirm("Erase everything and start over?")) {
        model_post({"cmd" : "file_new"}, load_song);
    }
}

function file_load() {
   var selectDialogueLink = $('<a href="">Select file</a>');
   var fileSelector = $('<input type="file">');
   $(fileSelector).change(function(event) {
        const reader = new FileReader();
        reader.onload = function() {
            model_post({
              "cmd": "data_load",
               "data" : { "file_contents" : reader.result }
            }, load_song, load_song);
        }
        reader.readAsText(event.target.files[0]);
   });
   selectDialogueLink.click(function(){
        fileSelector.click();
        return false;
   });
   selectDialogueLink.click()
}

function file_save_as() {
   edit_song()
   var filename = document.getElementById('filename').value;
   if (filename == "") {
       filename = "warp.json";
   }
   model_post({"cmd" : "file_save"}, function(data) {
      var filedata = JSON.stringify(data.data);
      var file = new Blob([filedata], {type: 'application/json'});
      var a = document.createElement("a");
      a.href = URL.createObjectURL(file);
      a.download = filename;
      a.click();
   });
}

function song_grid_cell_renderer(data) {
     var entry = data["value"];
     if (entry["type"] == "scene") {
         return "<a href='#' class='green_on_hover' onclick='play_scene(" + entry["scene_id"] + ")'><i class='fas fa-play'></i></a></a>&nbsp;&nbsp;&nbsp;<A HREF='#' onclick='load_into_nav(SCENE);load_scene_item(" + entry["scene_id"] + ")'>&nbsp;" + entry["scene_name"] + "</a>";
     }
     if (entry["type"] == "clip") {
         return "<a href='#' class='green_on_hover' onclick='play_clip(" + entry["clip_id"] + ")'><span class='clips_" + entry["clip_id"] + "_indicator'><i class='fas fa-play'></i></span></a>&nbsp;&nbsp;&nbsp;<A class='blue_on_hover' HREF='#' onclick='load_clip_item(" + entry["scene_id"] + "," + entry["track_id"] + ")'>&nbsp;&nbsp;" + entry["clip_name"] + "</a>";
     }
     if (entry["type"] == "empty_cell") {
         return "<a class='red_on_hover' href='#' onclick='stop_track(" + entry["track_id"] + ")'><i class='fas fa-stop'></i></a>&nbsp;&nbsp;&nbsp;<a class='blue_on_hover' href='#' onclick='new_clip(" + entry["scene_id"] + "," + entry["track_id"] + ")'>&nbsp;&nbsp;<i class='fas fa-plus'></i></a>&nbsp;";
     }
     return "??";
}

function delete_scenes(data, on_ok) {
    model_post({
         "cmd" : 'grid_for_song_delete_rows',
         "data" : data
    }, on_ok);
}

function update_song_grid(gridOptions) {

    var postback = "grid_for_song_postback";

    var state = gridOptions.columnApi.getColumnState();
    console.log("column state");
    console.log(state);

    // iterate through every node in the grid
    var results = [];
    gridOptions.api.forEachNode(function(rowNode, index) {
        results.push(rowNode.data);
    });
    model_post({
         "cmd" : postback,
         "data" : results
    }, function(ok_data) {
    });
}

function load_song_grid() {

   model_post({
       "cmd" : "grid_for_song",
   }, function(data) {

       var columnDefs = data["data"]["column_defs"];

       for(i=0; i<columnDefs.length; i++) {
           columnDefs[i]["cellRenderer"] = song_grid_cell_renderer;
       }

       var rowData = data["data"]["row_data"];
       var gridDiv = document.querySelector('#myGrid');

       gridDiv.innerHTML = '';

       var gridOptions = {

           columnDefs: columnDefs,
           rowData: rowData,
           rowDragManaged: true,
           enableMultiRowDragging: true,
           rowSelection: 'multiple',
           rowDeselection: true,
           animateRows: true,
           onGridReady: (params) => {
               gridOptions.api.sizeColumnsToFit();
           },
           onRowDragEnd: function(event) { console.log('on row drag end'); update_song_grid(gridOptions); },
       };

       new agGrid.Grid(gridDiv, gridOptions);

       $('#new_scene_button').on('click', function() {
            model_post({ "cmd" : "new_scene", data: {}}, function(data) {
                load_song();
            });
       });

       $('#new_track_button').on('click', function() {
            model_post({ "cmd" : "new_track", data: {}}, function(data) {
                load_song();
            });
       });

       $('#delete_scene_button').on('click', function() {
           items = [];
           var nodes = gridOptions.api.getSelectedNodes();
           for(i=0; i<nodes.length; i++) {
              //console.log(nodes[i]);
              items.push(nodes[i]["childIndex"]);
           }
           delete_scenes(items, function() { gridOptions.api.removeItems(gridOptions.api.getSelectedNodes()); });
       });
   });
}

/**********************************************************************************************************************/
/* SCALES                                                                                                             */
/**********************************************************************************************************************/

function clear_scale_type() {
   $('#scale_type').val(null).trigger('change');
}

function load_scale_item(item) {
    load_into_workspace(SCALE, item);
}

function new_scale_item() {
    model_do_new("scale");
}

function edit_scale(cb = null) {
    model_do_edit("scale",
        textboxes=["new_name"],
        selects=["note","scale_type"],
        multiple_selects=["slots"],
        toggles=[],
        ranges=[],
        cb = function() { load_scales(); }
    );
}

function delete_scale(item) {
    model_delete(SCALE, item);
}

function copy_scale(item) {
    model_copy(SCALE, item);
}

/**********************************************************************************************************************/
/* INSTRUMENTS                                                                                                        */
/**********************************************************************************************************************/

function load_instrument_item(item) {
    load_into_workspace(INSTRUMENT, item);
}

function new_instrument_item() {
    model_do_new("instrument");
}

function edit_instrument(cb = null) {
    model_do_edit(INSTRUMENT,
        textboxes=["new_name"],
        selects=["device", "channel",
        "drum1_note","drum2_note","drum3_note","drum4_note","drum5_note","drum6_note","drum7_note","drum8_note",
        "drum1_octave","drum2_octave","drum3_octave","drum4_octave","drum5_octave","drum6_octave","drum7_octave","drum8_octave"],
        multiple_selects=[],
        toggles=["muted"],
        ranges=["min_octave","max_octave","base_octave"],
        cb = function() { load_instruments(); }
    );
}

function delete_instrument(item) {
    model_delete(INSTRUMENT, item);
}

function copy_instrument(item) {
    model_copy(INSTRUMENT, item);
}

/**********************************************************************************************************************/
/* SCENES                                                                                                             */
/**********************************************************************************************************************/

function edit_scene(cb = null) {
    model_do_edit(SCENE,
        textboxes=["new_name"],
        selects=["scale"],
        multiple_selects=[],
        toggles=["auto_advance"],
        ranges=["rate"],
        cb = function() { load_scenes(); }
    );
}

function load_scene_item(item) {
    load_into_workspace(SCENE, item)
}

function load_clip_item(scene_id, track_id) {
    load_into_div("/pages/clip/" + scene_id + "," + track_id, WORKSPACE_DIV);
}

function new_scene_item() {
   model_do_new(SCENE);
}

function delete_scene(item) {
    model_delete(SCENE, item);
}

function copy_scene(item) {
    model_copy(SCENE, item);
}

function play_scene(item) {
    model_post({
       "cmd" : "play_scene",
       "id" : item
    }, function(data) {});
}

/**********************************************************************************************************************/
/* TRACKS                                                                                                             */
/**********************************************************************************************************************/

function stop_track(item) {
    model_post({
       "cmd" : "stop_track",
       "id" : item
    }, function(data) {});
}

function edit_track(cb = null) {
    model_do_edit(TRACK,
        textboxes=["new_name"],
        selects=["instrument_mode"],
        multiple_selects=["instruments"],
        toggles=["muted"],
        ranges=[],
        cb = function() { load_tracks(); }
    );
}

function load_track_item(item) {
    load_into_workspace(TRACK, item);
}

function new_track_item() {
   model_do_new(TRACK);
}

function delete_track(item) {
    model_delete(TRACK, item);
}

function copy_track(item) {
    model_copy(TRACK, item);
}

/**********************************************************************************************************************/
/* PATTERNS                                                                                                           */
/**********************************************************************************************************************/


function edit_pattern(cb = null) {
   model_do_edit(PATTERN,
        textboxes=["new_name", "rate"],
        selects=["scale","direction","pattern_type","audition_with","drum_config"],
        multiple_selects=[],
        toggles=[],
        ranges=["octave_shift"],
        cb = function() { load_patterns(); }
    );
}

function load_pattern_item(item) {
    load_into_workspace(PATTERN, item);
}

function new_pattern_item() {
    model_do_new(PATTERN);
}

function delete_pattern(item) {
   model_delete(PATTERN, item);
}

function copy_pattern(item) {
   model_copy(PATTERN, item);
}

function update_grid_backend(original_cmd, category, gridOptions, reload=null) {
    var postback = original_cmd + "_postback";
    var results = [];
    gridOptions.api.forEachNode(function(rowNode, index) {
        results.push(rowNode.data);
    });
    model_post({
         "cmd" : postback,
         "id" : document.getElementById("obj_id").value,
         "data" : results
    }, function(ok_data) {
        console.log("update complete");
        console.log(ok_data);
        if (reload != null) {
            reload(gridOptions, ok_data);
        }
    });
}

function delete_grid_nodes(original_cmd, rows) {
    var postback = original_cmd + "_delete_rows";
    model_post({
         "cmd" : postback,
         "id" : document.getElementById("obj_id").value,
         "data" : rows,
    }, function(ok_data) {
        console.log("its all good");
    });
}

function load_pattern_grid(category) {
    generic_grid_init('grid_for_pattern', category);
}

function load_pattern_common_grid() {
    load_pattern_grid('common');
    toggle_tab('pattern_common');
}

function load_pattern_pitch_grid() {
   load_pattern_grid('pitch');
   toggle_tab('pattern_pitch');
}

function load_pattern_time_grid() {
   load_pattern_grid('time');
   toggle_tab('pattern_time');
}

function load_pattern_modulation_grid() {
   load_pattern_grid('modulation');
   toggle_tab('pattern_mod');
}

function load_pattern_control_grid() {
   load_pattern_grid('control');
   toggle_tab('pattern_ctrl');
}

function load_pattern_variable_grid() {
   load_pattern_grid('variable');
   toggle_tab('pattern_vars');
}

function audition_pattern() {
    var obj_id = document.getElementById("obj_id").value;
    model_post({
       "cmd" : "audition_pattern",
       "id" : obj_id
   }, null);
}

/**********************************************************************************************************************/
/* CLIPS
/**********************************************************************************************************************/

function play_clip(item) {
    if (item == null) {
        item = document.getElementById("obj_id").value;
    }
    model_post({
       "cmd" : "play_clip",
       "id" : item
    }, function(data) {});
    selector = $(".clips_" + item + "_indicator");
    selector.removeClass("lights_inactive");
    selector.addClass("lights_active");
}

function audition_clip() {
    var obj_id = document.getElementById("obj_id").value;
    model_post({
       "cmd" : "audition_clip",
       "id" : obj_id
   }, null);
}

function new_clip(scene_id, track_id) {
    model_post({
         "cmd" : 'new_clip',
         "data" : { "scene_id" : scene_id, "track_id" : track_id }
    }, function(ok_data) {
         load_clip_item(scene_id, track_id);
    });
}

function edit_clip(cb = null) {
    model_do_edit(CLIP,
        textboxes=["new_name","rate","repeat","scene","track"],
        selects=[],
        multiple_selects=[],
        toggles=["auto_scene_advance"],
        ranges=[],
        cb = function() { load_tracks(); }
    );
}

function delete_clip(item) {
   model_delete(CLIP, item);
   load_song();
}

function reload_clip_grid(gridOptions, data) {

    var to_update = [];
    var ui_count = 0;
    var server_count = data['data']['row_data'].length;

    gridOptions.api.forEachNodeAfterFilterAndSort(function (row_node, index) {
        ui_count = ui_count + 1;
        var row_data = row_node.data;
        var server_data = data['data']['row_data'][index];
        var items = [ "audition","pattern", "transform1", "transform2", "transform3", "tempo_shift", "scale" ]
        for (i=0; i<items.length; i++) {
            var item = items[i];
            row_data[item] = server_data[item];
        }
        to_update.push(row_data);
    });

    gridOptions.api.applyTransaction({ update: to_update });
    if (ui_count != server_count) {
        gridOptions.api.applyTransaction({ add: [{}] });
    }
}

function audition_clip_slot(clip_id, slot_number) {
    console.log("audition_clip_slot: " + clip_id + "," + slot_number);
    model_post({
       "cmd" : "audition_clip_slot",
       "data" : {
           "clip_id" : clip_id,
           "slot_number": slot_number
       }
    }, null);
}

function clip_grid_renderer(entry) {
    var field = entry['colDef']['field'];
    if (field == 'audition') {
        if (entry['value'] == null) {
            return "";
        }
        var tokens = entry['value'].split(",");
        var clip = tokens[0];
        var slot = tokens[1];
        var pattern = tokens[2];
        return "<a href='#' class='green_on_hover' onclick='audition_clip_slot(" + clip + "," + slot + ")'><i class='fas fa-play'></i></a></a>&nbsp;&nbsp;&nbsp;<span class='patterns_" + pattern + "_indicator'><i class='fas fa-bolt'></i></span>";
    }
    return entry['value'];
}

function load_clip_grid() {
   generic_grid_init('grid_for_clip', 'null', 'myGrid', reload_clip_grid, clip_grid_renderer);
}


/**********************************************************************************************************************/
/* TRANSFORMS                                                                                                         */
/**********************************************************************************************************************/

function edit_transform(cb = null) {
   model_do_edit(TRANSFORM,
        textboxes=["new_name"],
        selects=["divide","direction","applies_to","audition_instrument","audition_pattern"],
        multiple_selects=[],
        toggles=["auto_reset","arp"],
        ranges=[],
        cb = function() { load_transforms(); }
    );
}

function load_transform_item(item) {
    load_into_workspace(TRANSFORM, item);
}

function new_transform_item() {
    model_do_new(TRANSFORM);
}

function delete_transform(item) {
   model_delete(TRANSFORM, item);
}

function copy_transform(item) {
   model_copy(TRANSFORM, item);
}

function audition_transform() {
    var obj_id = document.getElementById("obj_id").value;
    model_post({
       "cmd" : "audition_transform",
       "id" : obj_id
   }, null);
}

function load_transform_grid(category) {
    generic_grid_init('grid_for_transform', category);
}

function load_transform_pitch_grid() {
   load_transform_grid('pitch');
   toggle_tab('transform_pitch');
}

function load_transform_time_grid() {
   load_transform_grid('time');
   toggle_tab('transform_time');
}

function load_transform_modulation_grid() {
   load_transform_grid('modulation');
   toggle_tab('transform_mod');
}

function load_transform_control_grid() {
   load_transform_grid('control');
   toggle_tab('transform_ctrl');
}

function load_transform_variable_grid() {
   load_transform_grid('variable');
   toggle_tab('transform_vars');
}

/**********************************************************************************************************************/
/* DATA POOLS                                                                                                         */
/**********************************************************************************************************************/

function load_data_pool_grid() {
    generic_grid_init('grid_for_data_pool', 'generic');
}


function edit_data_pool(cb = null) {
   model_do_edit(DATA_POOL,
        textboxes=["new_name"],
        selects=["direction"],
        multiple_selects=[],
        toggles=[],
        ranges=[],
        cb = function() { load_data_pools(); }
    );
}

function load_data_pool_item(item) {
    load_into_workspace(DATA_POOL, item);
}

function new_data_pool_item() {
    model_do_new(DATA_POOL);
}

function delete_data_pool(item) {
    model_delete(DATA_POOL, item);
}

function copy_data_pool(item) {
    model_copy(DATA_POOL, item);
}

/**********************************************************************************************************************/
/* DEVICES                                                                                                             */
/**********************************************************************************************************************/

function load_device_item(item) {
    load_into_workspace(DEVICE, item);
}

/**********************************************************************************************************************/
/* MISC                                                                                                               */
/**********************************************************************************************************************/

function toggle_tab(tab_id) {
    var selector = $('.button_tab');
    selector.removeClass('button_tab_active');
    $("#" + tab_id).addClass('button_tab_active');
}

function toggle_lights(data_map, categories, on) {

    if (data_map == null) { data_map = playing_objects; }
    if (categories == null) { categories = OBJECT_CATEGORIES; }

    for (i=0; i<categories.length; i++) {
        var category = categories[i];

        for (j=0; j<data_map[category].length; j++) {
            var item = data_map[category][j];
            var className = "." + category + "_" + item + "_indicator";
            var selector = $(className);

            if (on) {
                //console.log('enabling selector: ' + className);
                selector.addClass("lights_active");
            } else {
                //console.log('disabling selector: ' + className);
                selector.removeClass("lights_active");
            }
        }
    }
}

function turn_on_lights(data_map, categories) {
    toggle_lights(data_map, categories, true);
}

function turn_off_lights(data_map, categories) {
    toggle_lights(data_map, categories, false);
}

function poll_status() {
    model_post({
         "cmd" : 'status_report',
         "data" : {}
    }, function(ok_data) {
         playing_objects = ok_data['data']['playing'];
         turn_on_lights(ok_data['data']['new_playing'], null);
         turn_off_lights(ok_data['data']['new_stopped'], null);
         window.setTimeout(poll_status, 333);
    });
}

$(document).ready(function() {
    console.log("warp engines online");
    load_initial_ui_state();
    console.log("take us out");
    window.setTimeout(poll_status, 1000);
});
