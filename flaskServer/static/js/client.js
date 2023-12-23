function isJSONObject(obj) {
    return typeof obj;
}

var source = new EventSource("/listen");
source.addEventListener('frame', function(event) {
    let data=event.data.replace(/'/g, '"');
    
    let ingest = JSON.parse(data);
    
    let imgData = ingest.img;
    
    

    
    pic.setAttribute('src', "data:image/jpg;base64," + imgData);
    
    let door = document.getElementById("lock");
    let lock = document.getElementById("door");


    lock.innerText = "lock: "+ingest.lock;
    door.innerText = "door: "+ingest.door;
            
   
        
}, false);