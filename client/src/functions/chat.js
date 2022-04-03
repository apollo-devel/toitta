export function chatName(chat, userLoggedIn) {
  if (!chat) {
    return "";
  }
  if (chat.name) {
    return chat.name;
  }
  return chat.users
    .filter((u) => u._id !== userLoggedIn._id)
    .map((u) => u.display_name)
    .join(", ");
}
