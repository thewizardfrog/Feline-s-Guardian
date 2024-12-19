/* 
  Popup - Resource Credit: https://github.com/WebDevSimplified/Vanilla-JavaScript-Modal/blob/master/script.js 
*/

const openPopUpButtons = document.querySelectorAll('[data-popup-target]')
const closePopUpButtons = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')

openPopUpButtons.forEach(button => {
  button.addEventListener('click', () => {
    const popup = document.querySelector(button.dataset.popupTarget)
    openPopUp(popup)
  })
})

closePopUpButtons.forEach(button => {
  button.addEventListener('click', () => {
    const popup = button.closest('.popup')
    closePopUp(popup)
  })
})

function openPopUp(popup) {
  if (popup == null) return
  popup.classList.add('active')
  overlay.classList.add('active')
}

function closePopUp(popup) {
  if (popup == null) return
  popup.classList.remove('active')
  overlay.classList.remove('active')
}

/* 
  Our achievement slideshow - Resource Credit: https://codepen.io/npayne/pen/LNNrOw 
*/

var slide;

$('div.back-img').click(function(){
  var slide = $('.nautilus img:last-child').remove();
  $('.nautilus').prepend(slide);
});

const deleteButton = document.getElementsByClassName('delete-button');
for (var i = 0; i < deleteButton.length; i++) {
    deleteButton[i].addEventListener('click', function() {
      this.parentNode.parentNode.parentNode.outerHTML = "";
  });
}



var card = document.querySelectorAll('.card')
var id = document.querySelectorAll('.card-header');
var issue = document.querySelectorAll('.card-title');
var real_name = document.querySelectorAll('.card-user');
var email = document.querySelectorAll('.card-email');
var telephone = document.querySelectorAll('.card-phone');

var list = [];

id.forEach(function(element, index) {
  var dict = {
    id: element.innerText,
    issue: issue[index].innerText,
    name: real_name[index].innerText,
    telephone: telephone[index].innerText,
    element: card[index]
  };
  list.push(dict)
});

const searchInput = document.querySelector('[data-search]');
if (searchInput != null) {
  searchInput.addEventListener('input', e => {
    const value = e.target.value;
    list.forEach((item) => {
      const isVisible = item.id.includes(value) || item.issue.includes(value.toUpperCase()) || item.name.includes(value) || item.telephone.includes(value);
      item.element.classList.toggle('hide', !isVisible);
    })
  })
}

/*
const productName = document.querySelectorAll('.atc-button');
productName.forEach(button => {
  button.addEventListener('click', () => {
    document.getElementById('order-summary-border').hidden = false;
  })
});
*/