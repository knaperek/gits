//the ONLY GLOBALS WE USE
var globals_array;
var globals;


//arrays
function node(id, type, x, y, url, ports, label) {
    this.id = id;
    this.type = type;
    this.x = x;
    this.y = y;
    this.url = url;
	this.ports = ports;
	this.label = label;
}

function edge(id, type, from, to, ax, ay, bx, by, porta, portb) {
    this.id = id;
    this.type = type;
    this.from = from;
    this.to = to;
    this.ax = ax;
    this.ay = ay;
    this.bx = bx;
    this.by = by;
	this.porta = porta;
	this.portb = portb;
}

function node_ports(ports) {
	this.ports = ports;
}

//other functions
function initialize_globals(){
	global = new Object();
	global.widget_id = -1;
	
	//-- counters and flags  and tmps ----
	global.drawing_line = null;
	global.click = null;
	global.tmp_point = null;
	global.tmp_node_id = null;
	
	global.deleting = null;
	global.line_style = 0;
	global.context_menu_count = 0;
	
	//----- Kinetic stuff vars  -----
	global.stage = null;
	global.image_layer = null;
	global.line_layer = null;
	global.edge_label = null;
	
	global.images_width = 100;
	global.images_height = 100;
	
	global.id_node = 0; //current ids
	global.id_edge = 0;
	
	//--------- JSON --------
	global.port_limits = null;
	global.current_node_index = null;
	global.current_port_index = null;
	global.JSONObject = null;
	
	// arrays
	global.edges = null;
	global.nodes = null;
	global.kedges = null;
	global.knodes = null;
	global.klabels = null;
	global.nodes_ports = null;
	
	return global;
}

function createStage(){
	 globals.stage = new Kinetic.Stage({
	  container: document.getElementsByClassName("container")[globals.widget_id],
	  width: document.getElementsByClassName("container")[globals.widget_id].clientWidth ,
	  height: document.getElementsByClassName("container")[globals.widget_id].clientHeight
	});
	
	globals.image_layer = new Kinetic.Layer();
	globals.line_layer = new Kinetic.Layer();
	
	globals.stage.add(globals.line_layer);	
	globals.stage.add(globals.image_layer);
	
	globals.edges = new Array();
    globals.nodes = new Array();
    globals.kedges = new Array();
    globals.knodes = new Array();
	globals.klabels = new Array();
	globals.nodes_ports = new Array();
}

function getTop(obj){
	var d = document.getElementsByClassName(obj)[globals.widget_id];
    var topValue= 0;
	
    while(d){
		topValue+= d.offsetTop;
		d = d.offsetParent;
    }
	
    return topValue;
}

function getLeft(obj){
	var d = document.getElementsByClassName(obj)[globals.widget_id];
    var leftValue= 0;
	
    while(d){
		leftValue+= d.offsetLeft;
		d= d.offsetParent;
    }
    
    return leftValue;
}

function drawLines(event, style) {

	event.preventDefault();

    globals.line_style = style;
    globals.drawing_line = true;
    document.body.style.cursor = 'crosshair';
	
	if(globals.deleting === true)
		trashClicked();
}

function cancelLines(event){

	if(event != null)
		event.preventDefault();

	globals.drawing_line = false;
	document.body.style.cursor = 'default';
	
	returnTakenPort();	
	CloseContext();
	globals.click = 0;
}

function trashClicked(event){
	if(event != null)
		event.preventDefault();

	 if(globals.deleting === false){
		  globals.deleting = true;
		  document.getElementsByClassName("button_trash")[globals.widget_id].src = JSONObject.others[2];
		  if(globals.drawing_line === true)
			cancelLines(null);
		document.body.style.cursor = 'no-drop';
	 }
	  else{
		  globals.deleting = false;
		  document.getElementsByClassName("button_trash")[globals.widget_id].src = JSONObject.others[1];
		  document.body.style.cursor = 'default';
	 }
	 returnTakenPort();
	 CloseContext();
}

function containerClicked(){
	globals.context_menu_count = globals.context_menu_count - 1;
	if (globals.context_menu_count == 0)
	{	
		returnTakenPort();
		CloseContext();
	}
}

function returnTakenPort(){
	try{
		if(globals.nodes_ports[globals.current_node_index].ports[globals.current_port_index] != -1 && globals.click == 1){
			globals.nodes_ports[globals.current_node_index].ports[globals.current_port_index] = globals.nodes_ports[globals.current_node_index].ports[globals.current_port_index] + 1;
			globals.click = 0;
		}
	}
	catch(err)
	{
		return;
	}
}

function setGlobals(event, id){
	var id_string = id.substring(6);
	var id_number = parseInt(id_string);
	
	globals = globals_array[id_number];
}


function refreshLayer(layer){
	layer.draw();
}

window.onscroll = function(){
	var element = document.getElementsByClassName("divContext")[globals.widget_id];
	element.style.display = 'none';
}

window.onload = function(){

	var inputs = document.getElementsByClassName("KineticField");
	var widget_count = inputs.length;
	var index = 0;
	var index2 = 0;
	
	globals_array = [];
	
	for(index = 0; index < widget_count; index++){
		
	globals_array[index] = initialize_globals();
	globals_array[index].widget_id = index;
	globals = globals_array[index];
	
	JSONLoad();	
	
	globals.drawing_line = false;
	globals.deleting = false;
	globals.click = 0;
	
	var div_context = document.createElement("div");
	div_context.setAttribute("class","divContext");	
	div_context.innerHTML = "";
	
	var div = document.getElementsByClassName("container")[globals.widget_id];
	div.appendChild(div_context);
	
	}
	
	document.getElementsByTagName('form')[0].setAttribute("onsubmit","Parse()");
}


