import { createStore } from 'vuex'
import router from '@/router';

import axios from 'axios';
import UIkit from 'uikit';

export default createStore({
  state: {
    userLoggedIn: undefined
  },
  getters: {
  },
  mutations: {
    setUserLoggedIn (state, user) {
      state.userLoggedIn = user;
    }
  },
  actions: {
    registerUser ({ commit }, user) {
      axios.post('/api/users', user).then(resp => {
        commit('setUserLoggedIn', resp.data);
        router.push('/');
      })
      .catch(error => {
        UIkit.notification(error.response.data.error.message, {status: 'danger'});
      });
    }
  },
  modules: {
  }
})
