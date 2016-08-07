  function activateModal(divModalId) {
    var modalDiv = document.createElement('div');
    modalDiv.style.width = '400px';
    modalDiv.style.height = '300px';
    modalDiv.style.margin = '100px auto';
    modalDiv.style.backgroundColor = '#fff';

    var modalContent = document.getElementById(divModalId);
    var cln = modalContent.cloneNode(true);
    cln.style.visibility = "visible";

    modalDiv.appendChild(cln);

    var options = {
        'keyboard': true,
        'static': false,
        'onclose': function() {
        }
      };

    mui.overlay('on', options, modalDiv);
  }