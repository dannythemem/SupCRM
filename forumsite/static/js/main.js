const profileBtn = document.getElementById('profileBtn');
const dropdownMenu = document.getElementById('dropdownMenu');

profileBtn.addEventListener('click', () => {
//  dropdownMenu.classList.toggle('hidden');
  dropdownMenu.classList.toggle('show');
});

document.addEventListener('click', (e) => {
  if (!profileBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
//    dropdownMenu.classList.add('show');
    dropdownMenu.classList.remove('show');
  }
});
