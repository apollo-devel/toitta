const imageUrl = user => {
  if (!user || !user.display_name) {
    return 'https://ui-avatars.com/api/?name=?';
  }

  if (!user.profile_pic) {
    return `https://ui-avatars.com/api/?name=${user.display_name}`;
  }
  return user.profile_pic;
}

export { imageUrl };