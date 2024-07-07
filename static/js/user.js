function openMenu(menuId) {
	closeAllMenus();

	var menu = document.getElementById(menuId);
	if (menu) {
	  menu.style.display = 'block';
	}
  }

  function closeAllMenus() {
	var menus = document.getElementsByClassName('menu');
	for (var i = 0; i < menus.length; i++) {
	  menus[i].style.display = 'none';
	}
  }