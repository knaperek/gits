function JSONLoad(){
	var div;
	var index = 0;
	var index2 = 0;
	
	//setting up HTML Elements
	var input = document.getElementsByClassName("KineticField")[globals.widget_id];
	var JSONstring;
	var html1 = '<p>Toolbox</p>';
	var html2 = '<p>Lines</p>';
	
	var div1 = document.createElement("div");
	div1.setAttribute("class","toolbox");
	div1.innerHTML = html1;
	
	var div2 = document.createElement("div");
	div2.setAttribute("class","lines");
	div2.innerHTML = html2;
	
	var div3 = document.createElement("div");
	div3.setAttribute("class","container");
	div3.setAttribute("ondrop","drop(event)");
	div3.setAttribute("ondragover","allowDrop(event)");
	div3.setAttribute("onclick","containerClicked(event)");
	div3.innerHTML = '';
	
	var div4 = document.createElement("div");
	div4.setAttribute("class","myWidget");	
	div4.setAttribute('id','widget' + globals.widget_id.toString());
	div4.setAttribute('onmouseover','setGlobals(event, this.id)');
	div4.setAttribute('onclick','AlertMouse(event)');
	div4.style.width = "auto";
	div4.style.height = "auto";
	div4.innerHTML = "";
	
	if (input.nextSibling) {
		input.parentNode.insertBefore(div4, input.nextSibling);
		div4.appendChild(div1);
		div4.appendChild(div2);		
		div4.appendChild(div3);
	}
	else {
		input.parentNode.appendChild(div4);
		div4.appendChild(div1);
		div4.appendChild(div2);
		div4.appendChild(div3);
	}
	
	//IMPORTANT
	createStage();
	globals.edge_label = new Kinetic.Text({
		x: 5,
        y: 5,
        text: " ",
        fontSize: 15,
        fontFamily: 'Calibri',
        fill: '#555',
        width: 700,
		margin: 0,
		padding: 0,
        align: 'left'
	});
	globals.image_layer.add(globals.edge_label);
	globals.image_layer.draw();
	//Proceeding to JSON load
	div = document.getElementsByClassName("toolbox")[globals.widget_id];
	
	JSONstring = input.value;
	JSONObject = eval('(' + JSONstring + ')');
	
	globals.JSONObject = JSONObject;
	
	loadImages(JSONObject.images);
	//--------------------------------------------------------------------------
	
	globals.port_limits = [];
	for(index; index < JSONObject.port_limits.length; index++)
	{
		globals.port_limits.push(JSONObject.port_limits[index].slice());
	}
	
	 //generate toolbox
	for(index = 0; index < JSONObject.images.length; index++)	{
		div.innerHTML=div.innerHTML +'\n' + '<img class="drag1" src="' + JSONObject.images[index] + '" draggable="true" ondragstart="drag(event)"></img>';
	}
	div.innerHTML = div.innerHTML + '\n' + '<button class="trash" onclick="trashClicked(event)">\n<img class="button_trash" src="' + JSONObject.others[1] + '" draggable="false" )"></img>\n</button>';
	
	//generate lines box
	div = document.getElementsByClassName("lines")[globals.widget_id];
	index = 0;
	/*
		PUT "no" into JSON if you don't want a type of line, but want some behind it
		0 - solid line black
		1 - dashed line black
		2 - solid line red
		3 - dashed line red
		4 - solid line cyan
		5 - dashed line cyan
		6 - smaller dashed line black
	*/
	for(index; index < JSONObject.lines.length; index++)	{
		if(JSONObject.lines[index] != "no"){
			div.innerHTML = div.innerHTML + '<button class="line" onclick="drawLines(event, ' + index + ')">\n<img class="button_image" src="' + JSONObject.lines[index] + '" draggable="false"></img>\n</button>';
		}
	}
	
	div.innerHTML = div.innerHTML + '<button class="line" onclick="cancelLines(event)">\n<img class="button_image" src="' + JSONObject.others[0] +'" draggable="false"></img>\n</button>';
	
	//try to load nodes and edges
	
	if(JSONObject.load == "no")
		return;
	else
	{
		//Proceed to loading
		index = 0;
		for(index; index < JSONObject.nodes.length; index++)
		{
			for(index2 = 0; index2 < JSONObject.edges.length; index2++)
			{
				if(JSONObject.nodes[index].id == JSONObject.edges[index2].from)
					JSONObject.edges[index2].from = globals.id_node;
				else if(JSONObject.nodes[index].id == JSONObject.edges[index2].to)
					JSONObject.edges[index2].to = globals.id_node;
			}
			loadNode(JSONObject.nodes[index]);
		}
		for(index = 0; index < JSONObject.edges.length; index++)
			loadEdge(JSONObject.edges[index]);
	
	}
	
	
}

function GetNodeNumber(src) {
	var index = 0;
	
	for(index; index < globals.JSONObject.images.length; index++)
		if (globals.JSONObject.images[index] == src.substring(src.length - globals.JSONObject.images[index].length))
			break;
			
	return index;
}

function GetNodeIndex(id) {
	
	var node_index = 0;
	
	for(node_index; node_index < globals.nodes.length; node_index++)
	{
		if(globals.knodes[node_index].attrs.id == id)
			break;
	}
	
	return node_index;
}

function GetEdgeIndex(id) {
	var edge_index = 0;
	
	for(edge_index; edge_index < globals.edges.length; edge_index++)
	{
		if(globals.kedges[edge_index].attrs.id == id)
			break;
	}
	
	return edge_index;
}
function removeX(array, ix){
	var index;
	var index2;
	var new_array = [];
	
	//dojdeme po ten co chceme zmazat
	for(index = 0; index < ix; index++){
		new_array[index] = array[index];
	}
	
	//preskocime nechceny
	index2 = index+1;
	
	for(index2; index2 < array.length; index2++, index++){
		new_array[index] = array[index2];
	}
	
	return new_array;
}


function loadImages(array){
	var images_objects;
	var img;
	var index;
	
	images_objects = [];
	for(index = 0; index < array.length; index++)
	{
		img = new Image();
		img.src = array[index];
		img.onload = function(){
			images_objects.push(img);
		}
	}	
}

function Parse(){
	var load;
	var string;
	var graph_data;
	var index;
	var index2;
	
	for(index = 0; index < globals_array.length; index++){
	
		if(globals_array[index].nodes.length > 0)
			load = "yes";
		else load= "no";

		//update node positions
		for(index2 = 0; index2 < globals_array[index].nodes.length; index2++){
			globals_array[index].nodes[index2].x = globals_array[index].knodes[index2].attrs.x;
			globals_array[index].nodes[index2].y = globals_array[index].knodes[index2].attrs.y;
		}
		//update edge positions
		for(index2 = 0; index2 < globals_array[index].edges.length; index2++){
			globals_array[index].edges[index2].ax = globals_array[index].kedges[index2].attrs.points[0].x;
			globals_array[index].edges[index2].ay = globals_array[index].kedges[index2].attrs.points[0].y;
			globals_array[index].edges[index2].bx = globals_array[index].kedges[index2].attrs.points[1].x;
			globals_array[index].edges[index2].by = globals_array[index].kedges[index2].attrs.points[1].y;
		}		
		
		//prepare old JSON object
		var input = document.getElementsByClassName("KineticField")[globals_array[index].widget_id];
		var value =  input.value ;
		
		JSON_new = eval('(' + value + ')');
		//generate new JSON object
		if(JSON_new.load == "no"){	//we had no nodes before
			if(load == "yes"){  //but we need to add some now
				
				JSON_new.nodes = globals_array[index].nodes;
				JSON_new.edges = globals_array[index].edges;
				JSON_new.load = "yes";
			}
		}
		else{ //we had nodes before
			if(load == "yes"){ //we need to update them
				JSON_new.nodes = globals_array[index].nodes;
				JSON_new.edges = globals_array[index].edges;
			}
			else{ //we need to delete them
				JSON_new.load = "no";
				delete JSON_new.nodes;
				delete JSON_new.edges;
			}
		}
		
		//parse new JSON string
		if(load == "yes")
			graph_data = {"images": JSON_new.images, "names": JSON_new.names,"lines": JSON_new.lines, "ports": JSON_new.ports, "port_limits": JSON_new.port_limits, "others": JSON_new.others, "load": JSON_new.load, "nodes": JSON_new.nodes, "edges": JSON_new.edges};
		else
			graph_data = {"images": JSON_new.images, "names": JSON_new.names, "lines": JSON_new.lines, "ports": JSON_new.ports, "port_limits": JSON_new.port_limits, "others": JSON_new.others,  "load": JSON_new.load};
		
		//check and write JSON string		
		string = JSON.stringify(graph_data);
		JSON_new = eval('(' + string + ')');
		input.value = string;
	}

}
