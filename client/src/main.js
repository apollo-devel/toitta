import UIkit from "uikit";
import Icons from "uikit/dist/js/uikit-icons";
import { createApp } from "vue";

import App from "./App.vue";
import router from "./router";
import store from "./store";

import "uikit/dist/css/uikit.min.css";
UIkit.use(Icons);

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.loginRequired)) {
    let user = store.state.userLoggedIn;
    if (user && user._id) {
      store.dispatch("loadUnreadNotifications");
      next();
    } else {
      await store.dispatch("loginCheck").catch(() => {
        // noop
      });
      user = store.state.userLoggedIn;
      if (user && user._id) {
        store.dispatch("loadUnreadNotifications");
        next();
      } else {
        next({ path: "/login" });
      }
    }
  } else {
    next();
  }
});

createApp(App).use(store).use(router).mount("#app");
