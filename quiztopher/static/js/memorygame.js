var mem_arr = ['Austria','Austria','Brazil','Brazil','Canada','Canada','Egypt','Egypt','France','France','Finland','Finland','Germany','Germany','India','India','Kuwait','Kuwait', 'New Zealand','New Zealand','Spain','Spain','USA','USA']; 
	var mem_val = [];
	var mem_tile_id = [];
	var tiles_flipped = 0;
	var no_of_times_flipped=0;
	Array.prototype.tile_shuffle = function(){
		var i = this.length, j, temp; 
		while(--i > 0)
		{ 
			j = Math.floor(Math.random() * (i+1));
			temp = this[j];
			this[j] = this[i]; 
			this[i] = temp; 
		} 
	} 
	var count=setInterval(timer,1000)
	function timer()
	{
		count += 1;
		document.getElementById('timer').innerHTML = count;
	}
	function newBoard(){ 
		tiles_flipped = 0; 
		var output = ''; 
		score = 0;
		count=0;
		mem_arr.tile_shuffle();
		for(var i = 0; i < mem_arr.length; i++){ 
			output += '<div id="tile_'+i+'" onclick="fliptile(this,\''+mem_arr[i]+'\')"></div>'; 
		} 
		document.getElementById('memory_board').innerHTML = output;
	}
	function fliptile(tile,val)
	{ 
		if(tile.innerHTML == "" && mem_val.length < 2)
		{ 
			tile.style.background = '#00FFFF';
			tile.style.font = "bold 20px Impact,Charcoal,sans-serif";
			tile.innerHTML = val;
			if(mem_val.length == 0)
			{ 
				mem_val.push(val); 
				mem_tile_id.push(tile.id); 
			} 
			else if(mem_val.length == 1)
			{ 
				mem_val.push(val);
				mem_tile_id.push(tile.id);
				if(mem_val[0] == mem_val[1])
				{   
				    	tiles_flipped += 2; // Clear both arrays 
				    	mem_val = []; 
				    	mem_tile_id = []; 
				    	// Check to see if the whole board is cleared 
				    	if(tiles_flipped == mem_arr.length)
				    	{ 
				    		//var continue=confirm("Do you want to play another game?")
				    		//if (continue==true)
				    		//{
				    			document.getElementById('memory_board').innerHTML = ""; 
				    			newBoard(); 
				    		//}
				    	} 
				    }
				    else 
				    { 
				    	function flipback()
				    	{ 
				    	// Flip the 2 tiles back over 
				    	var tile_1 = document.getElementById(mem_tile_id[0]); 
				    	var tile_2 = document.getElementById(mem_tile_id[1]);
				    	tile_1.style.background = 'url("{{=URL('static','images/country.jpg')}}") no-repeat';
				    	tile_1.style.backgroundSize = "100%"; 
				    	tile_1.innerHTML = "";
				    	tile_1.style.display="table-cell";
				    	tile_1.style.textAlign="center";
				    	tile_1.style.verticalAlign="middle";
				    	tile_2.style.background = 'url("{{=URL('static','images/country.jpg')}}") no-repeat';
				    	tile_2.style.backgroundSize = "100%"; 
				    	tile_2.innerHTML = ""; 
				    	mem_val = [];
				    	mem_tile_id = []; 
				    } 
				    setTimeout(flipback, 500); 
				}
			} 
		} 
	} 
	
newBoard();
