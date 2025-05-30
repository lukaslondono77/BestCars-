const isAuthenticated = () => {
  return sessionStorage.getItem('username') !== null;
}; 