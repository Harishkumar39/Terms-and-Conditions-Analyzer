//// background.js
//chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
//  if (request.action === 'readPage') {
//    fetch('http://localhost:5000/read_page', {
//      method: 'POST',
//      headers: {
//        'Content-Type': 'application/json',
//      },
//      body: JSON.stringify(request),
//    })
//      .then(response => response.json())
//      .then(data => {
////        tabId = sender.id
//        //console.log(typeof data.resultant)
//        //let myObject = data.resultant
//        //let propertyList = Object.entries(myObject);
//        console.log(data.resultant)
//        sendResponse({data:data.resultant})
////        console.log(chrome.tabs);
////        console.log(sender)
////        chrome.tabs.sendMessage(request.tab.id, { action: 'displayResult', data: data.resultant });
//
//      })
//      .catch(error => {
//        console.error('Error:', error);
//      });
//  }
//});

//// background.js

chrome.runtime.onConnect.addListener(function(port) {
  console.assert(port.name === 'popup');

  port.onMessage.addListener(function(msg) {
    if (msg.action === 'readPage') {
      fetch('http://localhost:5000/read_page', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(msg),
      })
        .then(response => response.json())
        .then(data => {
          // Send the data back to the popup through the port
          port.postMessage({ action: 'displayResult', data: data });
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  });
});


