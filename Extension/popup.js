//// popup.js

document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('h1').textContent = 'Terms and Conditions Analyzer';

  // Connect to the background script
  const port = chrome.runtime.connect({ name: 'popup' });

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentTab = tabs[0];
    console.log(tabs[0])

    // Send a message through the port to initiate the communication
    port.postMessage({ action: 'readPage', tab: currentTab });

    // Listen for messages from the background script
    port.onMessage.addListener(function (response) {

      const final_data = response.data

      const groupedData = {
          "Not Risky": [],
          "Very Risky": [],
          "Risky": []
      };

      for (const statement in final_data.resultant) {
          const riskLevel = final_data.resultant[statement];
          groupedData[riskLevel].push(statement);
      }

      console.log(groupedData)

      const very_risky = document.getElementById('very-risky');
      const risky = document.getElementById('risky');
      const not_risky = document.getElementById('not-risky');

      //resultContainer.textContent = `Server Response: ${JSON.stringify(response)}`;
      very_risky.textContent = `${groupedData['Very Risky'].slice(0,3)}`
      risky.textContent = `${groupedData['Risky'].slice(0,3)}`
      not_risky.textContent = `${groupedData['Not Risky'].slice(0,3)}`
    });
  });
});
