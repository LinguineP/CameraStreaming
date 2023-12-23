function isJSONObject(obj) {
    return typeof obj;
}

var source = new EventSource("/listen");
source.addEventListener('frame', function(event) {
    let data=event.data.replace(/'/g, '"');
    let ingest = JSON.parse(JSON.parse(data));
    
    var imgData = ingest.img;


    var imgBytes = atob(imgData);
    pic.setAttribute('src', "data:image/jpg;base64," + imgData);
   
        
}, false);