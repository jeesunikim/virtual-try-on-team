document.getElementById('overlayButton').addEventListener('click', function() {
  const overlayInput = document.getElementById('overlayInput');
  if (overlayInput.files.length > 0) {
    const imageUrl = URL.createObjectURL(overlayInput.files[0]);
    chrome.runtime.sendMessage({ action: 'overlayImage', imageUrl });
  }
});
