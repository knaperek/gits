function GetContext(src, x, y, height, width, id){
	var index = 0;
	var index2 = 0;
	var div;
	var node_index;
	//search for node source
	for(index; index < globals.JSONObject.images.length; index++)
		if (globals.JSONObject.images[index] == src.substring(src.length - globals.JSONObject.images[index].length))
			break;
			
	//search for node index in knodes array		
	node_index = GetNodeIndex(id);
	
	//try to generate HTML for context menu		
	if(index >= globals.JSONObject.images.length)
		return;
	else
	{
		div = document.getElementsByClassName("divContext")[globals.widget_id];
		div.innerHTML = '<ul class="cmenu">\n';
		
		for(index2; index2 < globals.JSONObject.ports[index].length; index2++)
		{
			if(globals.nodes_ports[node_index].ports[index2] != 0)
				div.innerHTML = div.innerHTML + '<li onclick="drawEdges(' + x + ',' + y + ',' + height + ',' + width + ',' + id + ',' + index2 + ',event)"><a href="#">' + globals.JSONObject.ports[index][index2] + '</a></li>\n';
			else
				div.innerHTML = div.innerHTML + '<li>' + globals.JSONObject.ports[index][index2] + '</li>\n';
		}
		div.innerHTML = div.innerHTML + '</ul>\n';
	}
}

function ContextShow(evt){
	var div = document.getElementsByClassName("divContext")[globals.widget_id];
	var div2 = document.getElementsByClassName("container")[globals.widget_id];
	var r;
	var element;
	
	// document.body.scrollTop does not work in IE
        var scrollTop = document.body.scrollTop ? document.body.scrollTop :
            document.documentElement.scrollTop;
        var scrollLeft = document.body.scrollLeft ? document.body.scrollLeft :
            document.documentElement.scrollLeft;
	
	div.style.display = 'none';
	div.style.left = evt.pageX - scrollLeft + "px";
	div.style.top = evt.pageY - scrollTop + "px";
	div.style.display = 'block';
}

function CloseContext(){
	var div = document.getElementsByClassName("divContext")[globals.widget_id];
    div.style.display = 'none';
}




