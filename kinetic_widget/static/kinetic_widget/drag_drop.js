function allowDrop(ev) {
	ev.preventDefault();
 }

 function drag(ev) {
	if(globals.drawing_line === true){
		cancelLines(null);
	}
	ev.dataTransfer.setData("Text",ev.target.src);
 }

 function drop(ev) {
	ev.preventDefault();
	var data_img=ev.dataTransfer.getData("Text");
	var container = document.getElementsByClassName("container")[globals.widget_id];
	var imageObj = new Image();
	
	imageObj.src = data_img;
	imageObj.width = globals.images_width;
	imageObj.height = globals.images_height;
	
	//calculate position
	var tempX = ev.pageX;
	var tempY = ev.pageY;
	var containerX = getLeft("container");
	var containerY = getTop("container");
	var finalX = tempX - containerX - (imageObj.width / 2);
	var finalY = tempY - containerY - (imageObj.height / 2);
	//fuck IE 10
	if ((tempX - containerX) < 0 || (tempX-getLeft("container")) > container.offsetWidth || (tempY - containerY) < 0 || (tempY-getTop("container")) > container.offsetHeight ){
		finalX = container.offsetWidth / 2 - (imageObj.width / 2);
		finalY = container.offsetHeight / 2 - (imageObj.height / 2);
	}
	var type = GetNodeNumber(data_img);		
	var label = globals.JSONObject.names[GetNodeNumber(data_img)] + " " + globals.id_node;
	
	// new image
    globals.knodes[globals.knodes.length] = new Kinetic.Image({
        image: imageObj,
        x: finalX,
        y: finalY,
        width: globals.images_width,
        height: globals.images_height,
        draggable: true,
        id: globals.id_node
    });
	//set up label
	globals.klabels[globals.klabels.length] = new Kinetic.Text({
        x: finalX,
        y: finalY + globals.images_height,
        text: label,
        fontSize: 18,
        fontFamily: 'Calibri',
        fill: '#555',
		margin: 0,
		padding: 0,
        align: 'center'
      });
	//label double click  
	globals.klabels[globals.klabels.length - 1].on("dblclick", function(evt){
		var index;
		//search for label position
		for(index = 0; index < globals.klabels.length; index++)
			if(globals.klabels[index] == this)
				break;
				
		var result = prompt("Give new name:", globals.nodes[index].label);
		this.setText(result);
		globals.nodes[index].label = result;
		globals.image_layer.draw();
	});
	//image events
	globals.knodes[globals.knodes.length - 1].on("click", function(evt){
        if (globals.drawing_line === true) {
			GetContext(this.attrs.image.src, this.attrs.x,this.attrs.y,this.attrs.height,this.attrs.width,this.attrs.id);
			ContextShow(evt);
			globals.context_menu_count = 3;            
        }
		else if(globals.deleting === true) {
			deleteNode(this.attrs.id);
		}
    });

    globals.knodes[globals.knodes.length - 1].on("dragmove", function() {
		var tmppoints;
		var index = GetNodeIndex(this.attrs.id);
		
        for (var i = 0; i < globals.edges.length; i++) {
            if (globals.edges[i].from === this.attrs.id) {
                tmppoints = globals.kedges[i].getPoints();
                tmppoints[0].x = this.getX() + (globals.images_width / 2);
                tmppoints[0].y = this.getY() + (globals.images_width / 2);
                globals.kedges[i].setPoints(tmppoints);
            }
            else if (globals.edges[i].to === this.attrs.id) {
                tmppoints = globals.kedges[i].getPoints();
                tmppoints[1].x = this.getX() + (globals.images_width / 2);
                tmppoints[1].y = this.getY() + (globals.images_width / 2);
                globals.kedges[i].setPoints(tmppoints);
            }	
        }
		//adjust label
		globals.klabels[index].attrs.x = this.getX();
		globals.klabels[index].attrs.y = this.getY() + globals.images_height;
		
		globals.line_layer.draw();	
    });
	
	globals.knodes[globals.knodes.length - 1].on("dragend", function() {
		globals.line_layer.draw();
	});

	// add cursor styling
	globals.knodes[globals.knodes.length - 1].on('mouseover', function() {
		if(globals.drawing_line === false && globals.deleting === false)
			document.body.style.cursor = 'pointer';
	});
	globals.knodes[globals.knodes.length - 1].on('mouseout', function() {
		if(globals.drawing_line === false && globals.deleting === false)
			document.body.style.cursor = 'default';
	});
	
	
	globals.nodes_ports[globals.knodes.length - 1] = new node_ports(globals.port_limits[GetNodeNumber(data_img)].slice());
    globals.nodes[globals.knodes.length - 1] = new node(globals.knodes[globals.knodes.length - 1].attrs.id, type, finalX, finalY, data_img, globals.nodes_ports[globals.knodes.length - 1], label);
       
    //draw image to image layer
    globals.image_layer.add(globals.knodes[globals.knodes.length - 1]);
	globals.image_layer.add(globals.klabels[globals.knodes.length - 1]);
    globals.image_layer.draw();
    globals.id_node++; 
 }
 
 function drawEdges(x, y, height, width, id, index,event) {
	event.preventDefault();
 
	var node_index;
	node_index = GetNodeIndex(id);
 
	if (globals.click === 0) {
		globals.tmp_point = new Array();
		globals.tmp_point[0] = x + (width / 2);
		globals.tmp_point[1] = y + (height / 2);
		globals.click = 1;
		globals.tmp_node_id = id;
		
		//port limit calculation
		if(globals.nodes_ports[node_index].ports[index] != -1)
			globals.nodes_ports[node_index].ports[index] = globals.nodes_ports[node_index].ports[index] - 1;
		globals.current_node_index = node_index;
		globals.current_port_index = index;
	}
	else {
		var dash;
		var color;
		
		if(globals.line_style === 0){
			dash = [30, 0];
			color = 'black'
		} else if(globals.line_style === 1){
			dash = [15, 5];
			color = 'black'
		} else if(globals.line_style === 2){
			dash = [30, 0];
			color = 'red'
		} else if(globals.line_style === 3){
			dash = [15, 5];
			color = 'red'
		} else if(globals.line_style === 4){
			dash = [30, 0];
			color = 'cyan'
		} else if(globals.line_style === 5){
			dash = [15, 5];
			color = 'cyan'
		} else if(globals.line_style === 6){
			dashArray: [29, 20, 0.001, 20]
			color = 'black'
		} else {
			dash = [5, 5];
			color = 'black';
		}
		globals.kedges[globals.kedges.length] = new Kinetic.Line({
			points: [globals.tmp_point[0], globals.tmp_point[1], x + (width / 2), y + (height / 2)],
			stroke: color,
			strokeWidth: 8,
			lineCap: 'miter',
			lineJoin: 'butt',
			id : globals.id_edge,
			dashArray : dash
		});
		globals.edges[globals.edges.length] = new edge(globals.id_edge, globals.line_style, globals.tmp_node_id, id, globals.tmp_point[0], globals.tmp_point[1], x + (width / 2), y + (height / 2),globals.current_port_index, index);
		
		//EVENT
		globals.kedges[globals.kedges.length - 1].on('click', function() {
			if(globals.deleting === true)
			{
				deleteEdge(this.attrs.id);
			}
		});
		
		globals.kedges[globals.kedges.length - 1].on('mouseover', function() {
			var edge_index, from_node_index, to_node_index;
			var from_node_src, to_node_src;
			
			//search for edge
			edge_index = GetEdgeIndex(this.attrs.id);
			//search for nodes indexes
			from_node_index = GetNodeIndex(globals.edges[edge_index].from);
			to_node_index = GetNodeIndex(globals.edges[edge_index].to);
			
			from_node_src = GetNodeNumber(globals.nodes[from_node_index].url);
			to_node_src = GetNodeNumber(globals.nodes[to_node_index].url);
			
			globals.edge_label.setText(globals.nodes[from_node_index].label + " : " + globals.JSONObject.ports[from_node_src][globals.edges[edge_index].porta] + " <-----> " + globals.nodes[to_node_index].label + " : " + globals.JSONObject.ports[to_node_src][globals.edges[edge_index].portb]);
			globals.image_layer.draw();
		});
		
		globals.kedges[globals.kedges.length - 1].on('mouseleave', function() {
		
			globals.edge_label.setText(" ");
			globals.image_layer.draw();
		});
		
		
		//port limit calculation
		if(globals.nodes_ports[node_index].ports[index] != -1)
			globals.nodes_ports[node_index].ports[index] = globals.nodes_ports[node_index].ports[index] - 1;
		globals.current_node_index = node_index;
		globals.current_port_index = index;

		globals.line_layer.add(globals.kedges[globals.kedges.length - 1]);
		globals.line_layer.draw();
		globals.click = 0;

		globals.id_edge++;
	}	
	CloseContext();
 }
 
 function deleteNode(id){
	var node_index = GetNodeIndex(id);
	globals.knodes[node_index].destroy();
	
	
	
	for (var i = 0; i < globals.kedges.length; i++) {
	
		if (globals.edges[i].from === id) {
			globals.kedges[i].destroy();
			globals.kedges.splice(i,1);
			
			if (globals.nodes_ports[GetNodeIndex(globals.edges[i].to)].ports[globals.edges[i].portb] != -1)
				globals.nodes_ports[GetNodeIndex(globals.edges[i].to)].ports[globals.edges[i].portb]++;
			
			globals.edges.splice(i,1);
			i--;
			}
		else if (globals.edges[i].to === id) {
			globals.kedges[i].destroy();
			globals.kedges.splice(i,1);
			
			if (globals.nodes_ports[GetNodeIndex(globals.edges[i].from)].ports[globals.edges[i].porta] != -1)
				globals.nodes_ports[GetNodeIndex(globals.edges[i].from)].ports[globals.edges[i].porta]++;
			
			globals.edges.splice(i,1);
			i--;
			}
		}
		
	
	globals.nodes_ports.splice(node_index,1);
	
	globals.klabels[node_index].destroy();
	globals.klabels.splice(node_index,1);
	
	globals.knodes.splice(node_index,1);
	globals.nodes.splice(node_index,1);
	
	globals.image_layer.draw();
	globals.line_layer.draw();
 }
 
 function deleteEdge(id){
	var edge_index = GetEdgeIndex(id);
	globals.kedges[edge_index].destroy();
	globals.kedges.splice(edge_index, 1);

	
	var from_node_index = GetNodeIndex(globals.edges[edge_index].from);
	var to_node_index = GetNodeIndex(globals.edges[edge_index].to);
	
	if (globals.nodes_ports[from_node_index].ports[globals.edges[edge_index].porta] != -1)
		globals.nodes_ports[from_node_index].ports[globals.edges[edge_index].porta]++;
		
	if (globals.nodes_ports[to_node_index].ports[globals.edges[edge_index].portb] != -1)	
		globals.nodes_ports[to_node_index].ports[globals.edges[edge_index].portb]++;
	
	globals.edges.splice(edge_index, 1);
	
	globals.line_layer.draw();
 }
 
 function loadNode(old_node){
		
	var data_img = old_node.url;
	var type;
	var container = document.getElementsByClassName("container")[globals.widget_id];
	var imageObj = new Image();
	
	imageObj.onload = function(){ 
		refreshLayer(globals.image_layer);
	}
	imageObj.src = data_img;
	imageObj.width = globals.images_width;
	imageObj.height = globals.images_height;
	
	var finalX = old_node.x;
	var finalY = old_node.y;
	type = GetNodeNumber(data_img);
	
	
	// new image
    globals.knodes[globals.knodes.length] = new Kinetic.Image({
        image: imageObj,
        x: finalX,
        y: finalY,
        width: globals.images_width,
        height: globals.images_height,
        draggable: true,
        id: globals.id_node
    });
	//set up label
	globals.klabels[globals.klabels.length] = new Kinetic.Text({
        x: finalX,
        y: finalY + globals.images_height,
        text: old_node.label,
        fontSize: 18,
        fontFamily: 'Calibri',
        fill: '#555',
		margin: 0,
		padding: 0,
        align: 'center'
      });
	//label double click  
	globals.klabels[globals.klabels.length - 1].on("dblclick", function(evt){
		var index;
		//search for label position
		for(index = 0; index < globals.klabels.length; index++)
			if(globals.klabels[index] == this)
				break;
				
		var result = prompt("Give new name:", globals.nodes[index].label);
		this.setText(result);
		globals.nodes[index].label = result;
		globals.image_layer.draw();
	});
	//image events
	globals.knodes[globals.knodes.length - 1].on("click", function(evt){
        if (globals.drawing_line === true) {
			GetContext(this.attrs.image.src, this.attrs.x,this.attrs.y,this.attrs.height,this.attrs.width,this.attrs.id);
			ContextShow(evt);
			globals.context_menu_count = 3;            
        }
		else if(globals.deleting === true) {
			deleteNode(this.attrs.id);
		}
    });

    globals.knodes[globals.knodes.length - 1].on("dragmove", function() {
		var tmppoints;
		var index = GetNodeIndex(this.attrs.id);
		
        for (var i = 0; i < globals.edges.length; i++) {
            if (globals.edges[i].from === this.attrs.id) {
                tmppoints = globals.kedges[i].getPoints();
                tmppoints[0].x = this.getX() + (globals.images_width / 2);
                tmppoints[0].y = this.getY() + (globals.images_width / 2);
                globals.kedges[i].setPoints(tmppoints);
            }
            else if (globals.edges[i].to === this.attrs.id) {
                tmppoints = globals.kedges[i].getPoints();
                tmppoints[1].x = this.getX() + (globals.images_width / 2);
                tmppoints[1].y = this.getY() + (globals.images_width / 2);
                globals.kedges[i].setPoints(tmppoints);
            }	
        }
        //adjust label
		globals.klabels[index].attrs.x = this.getX();
		globals.klabels[index].attrs.y = this.getY() + globals.images_height;
		
        globals.line_layer.draw();      
    });
	
	globals.knodes[globals.knodes.length - 1].on("dragend", function() {
		globals.line_layer.draw();
	});
	
	// add cursor styling
	globals.knodes[globals.knodes.length - 1].on('mouseover', function() {
		if(globals.drawing_line === false && globals.deleting === false)
			document.body.style.cursor = 'pointer';
	});
	globals.knodes[globals.knodes.length - 1].on('mouseout', function() {
		if(globals.drawing_line === false && globals.deleting === false)
			document.body.style.cursor = 'default';
	});	
	
	globals.nodes_ports[globals.nodes.length] = old_node.ports;
	globals.nodes[globals.nodes.length] = new node(globals.knodes[globals.id_node].attrs.id, type, old_node.x, old_node.y, old_node.url, old_node.ports, old_node.label);
       
    //draw image to image layer
    globals.image_layer.add(globals.knodes[globals.knodes.length - 1]);
	globals.image_layer.add(globals.klabels[globals.klabels.length - 1]);
	globals.image_layer.draw();
    globals.id_node++;
 }
 
 function loadEdge(old_edge){
	var dash;
	var color;
	
	if(old_edge.type === 0){
		dash = [30, 0];
		color = 'black'
	} else if(old_edge.type === 1){
		dash = [15, 5];
		color = 'black'
	} else if(old_edge.type === 2){
		dash = [30, 0];
		color = 'red'
	} else if(old_edge.type === 3){
		dash = [15, 5];
		color = 'red'
	} else if(old_edge.type === 4){
		dash = [30, 0];
		color = 'cyan'
	} else if(old_edge.type === 5){
		dash = [15, 5];
		color = 'cyan'
	} else if(old_edge.type === 6){
		dashArray: [29, 20, 0.001, 20]
		color = 'black'
	} else {
		dash = [5, 5];
		color = 'black';
	}
		
	globals.kedges[globals.kedges.length] = new Kinetic.Line({
		points: [old_edge.ax, old_edge.ay, old_edge.bx, old_edge.by],
		stroke: color,
		strokeWidth: 8,
		lineCap: 'miter',
		lineJoin: 'butt',
		id : globals.id_edge,
		dashArray : dash
	});
	//EVENT
	globals.kedges[globals.kedges.length - 1].on('click', function() {
	if(globals.deleting === true)
	{
		deleteEdge(this.attrs.id);
	}
	});
		
	globals.kedges[globals.kedges.length - 1].on('mouseover', function() {
			var edge_index, from_node_index, to_node_index;
			var from_node_src, to_node_src;
			
			//search for edge
			edge_index = GetEdgeIndex(this.attrs.id);
			//search for nodes indexes
			from_node_index = GetNodeIndex(globals.edges[edge_index].from);
			to_node_index = GetNodeIndex(globals.edges[edge_index].to);
			
			from_node_src = GetNodeNumber(globals.nodes[from_node_index].url);
			to_node_src = GetNodeNumber(globals.nodes[to_node_index].url);
			
			globals.edge_label.setText(globals.nodes[from_node_index].label + " : " + globals.JSONObject.ports[from_node_src][globals.edges[edge_index].porta] + " <-----> " + globals.nodes[to_node_index].label + " : " + globals.JSONObject.ports[to_node_src][globals.edges[edge_index].portb]);
			globals.image_layer.draw();
		});
		
		
	globals.kedges[globals.kedges.length - 1].on('mouseleave', function() {
		
			globals.edge_label.setText(" ");
			globals.image_layer.draw();
		});
	
	
	globals.edges[globals.edges.length] = new edge(globals.id_edge, old_edge.type, old_edge.from, old_edge.to, old_edge.ax, old_edge.ay, old_edge.bx, old_edge.by, old_edge.porta, old_edge.portb);

	globals.line_layer.add(globals.kedges[globals.kedges.length - 1]);
	globals.line_layer.draw();
	globals.image_layer.draw();

	globals.id_edge++;
		
 }
 