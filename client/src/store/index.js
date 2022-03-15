import { createStore } from 'vuex'
import router from '@/router';

import axios from 'axios';
import UIkit from 'uikit';

export default createStore({
  state: {
    userLoggedIn: undefined,
    posts: []
  },
  getters: {
  },
  mutations: {
    setUserLoggedIn (state, user) {
      state.userLoggedIn = user;
    },
    setPosts (state, posts) {
      state.posts = posts;
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
    },
    login ({ commit }, credential) {
      axios.post('/api/login', credential).then(resp => {
        commit('setUserLoggedIn', resp.data);
        router.push('/');
      })
      .catch(error => {
        UIkit.notification(error.response.data.error.message, {status: 'danger'});
      });
    },
    logout ({ commit }) {
      axios.post('/api/logout').then(() => {
        commit('setUserLoggedIn', undefined);
        router.push('/login');
      })
      .catch(error => {
        UIkit.notification(error.response.data.error.message, {status: 'danger'});
      });
    },
    createPost ({ state }, content) {
      const body = {
        content,
        posted_by: state.userLoggedIn._id
      };
      return axios.post('/api/posts', body)
        .then(() => {
          return true;
        })
        .catch(error => {
          UIkit.notification(error.response.data.error.message, {status: 'danger'});
          return false;
        });
    },
    loadPosts ({ commit }) {
      axios.get('/api/posts').then(resp => {
        commit('setPosts', resp.data);
      })
      .catch(error => {
        if (error.response.status === 401) {
          router.push('/login');
        } else {
          UIkit.notification(error.response.data.error.message, {status: 'danger'});
        }
      });
    }
  },
  modules: {
  }
})
