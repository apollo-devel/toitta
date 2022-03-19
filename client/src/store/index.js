import axios from "axios";
import UIkit from "uikit";
import { createStore } from "vuex";

import router from "@/router";

export default createStore({
  state: {
    userLoggedIn: undefined,
    posts: [],
    profile: {
      user: {
        display_name: "",
        username: "",
      },
    },
  },
  getters: {},
  mutations: {
    setUserLoggedIn(state, user) {
      state.userLoggedIn = user;
    },
    setPosts(state, posts) {
      state.posts = posts;
    },
    updatePost(state, post) {
      const orig = state.posts.find((p) => p._id === post._id);
      if (orig) {
        Object.assign(orig, post);
      }
      state.posts
        .filter((p) => p.retweeted_post && p.retweeted_post._id === post._id)
        .forEach((p) => Object.assign(p.retweeted_post, post));
    },
    setProfileUser(state, user) {
      state.profile.user = user;
    },
  },
  actions: {
    registerUser({ commit }, user) {
      axios
        .post("/api/users", user)
        .then((resp) => {
          commit("setUserLoggedIn", resp.data);
          router.push("/");
        })
        .catch((error) => {
          UIkit.notification(error.response.data.error.message, {
            status: "danger",
          });
        });
    },
    login({ commit }, credential) {
      axios
        .post("/api/login", credential)
        .then((resp) => {
          commit("setUserLoggedIn", resp.data);
          router.push("/");
        })
        .catch((error) => {
          UIkit.notification(error.response.data.error.message, {
            status: "danger",
          });
        });
    },
    logout({ commit }) {
      axios
        .post("/api/logout")
        .then(() => {
          commit("setUserLoggedIn", undefined);
          router.push("/login");
        })
        .catch((error) => {
          UIkit.notification(error.response.data.error.message, {
            status: "danger",
          });
        });
    },
    async loginCheck({ commit }) {
      const resp = await axios.get("/api/session");
      commit("setUserLoggedIn", resp.data);
    },
    async createPost({ state }, content) {
      const body = {
        content,
        posted_by: state.userLoggedIn._id,
      };
      return axios
        .post("/api/posts", body)
        .then(() => {
          return true;
        })
        .catch((error) => {
          UIkit.notification(error.response.data.error.message, {
            status: "danger",
          });
          return false;
        });
    },
    loadPosts({ commit }) {
      axios
        .get("/api/posts")
        .then((resp) => {
          commit("setPosts", resp.data);
        })
        .catch((error) => {
          if (error.response.status === 401) {
            router.push("/login");
          } else {
            UIkit.notification(error.response.data.error.message, {
              status: "danger",
            });
          }
        });
    },
    likePost({ commit }, post) {
      axios
        .post(`/api/posts/${post._id}/like`)
        .then((resp) => {
          commit("updatePost", resp.data);
        })
        .catch((error) => {
          if (error.response.status === 401) {
            router.push("/login");
          } else {
            UIkit.notification(error.response.data.error.message, {
              status: "danger",
            });
          }
        });
    },
    unlikePost({ commit }, post) {
      axios
        .delete(`/api/posts/${post._id}/like`)
        .then((resp) => {
          commit("updatePost", resp.data);
        })
        .catch((error) => {
          if (error.response.status === 401) {
            router.push("/login");
          } else {
            UIkit.notification(error.response.data.error.message, {
              status: "danger",
            });
          }
        });
    },
    retweetPost({ commit }, post) {
      axios
        .post(`/api/posts/${post._id}/retweet`)
        .then((resp) => {
          commit("updatePost", resp.data);
        })
        .catch((error) => {
          if (error.response.status === 401) {
            router.push("/login");
          } else {
            UIkit.notification(error.response.data.error.message, {
              status: "danger",
            });
          }
        });
    },
    unretweetPost({ commit }, post) {
      axios
        .delete(`/api/posts/${post._id}/retweet`)
        .then((resp) => {
          commit("updatePost", resp.data);
        })
        .catch((error) => {
          if (error.response.status === 401) {
            router.push("/login");
          } else {
            UIkit.notification(error.response.data.error.message, {
              status: "danger",
            });
          }
        });
    },
    loadProfileUser({ commit }, username) {
      return axios.get(`/api/users/${username}`).then((resp) => {
        commit("setProfileUser", resp.data);
      });
    },
    followUser({ commit }, username) {
      return axios.post(`/api/users/${username}/follow`).then((resp) => {
        commit("setUserLoggedIn", resp.data);
      });
    },
    unfollowUser({ commit }, username) {
      return axios.delete(`/api/users/${username}/follow`).then((resp) => {
        commit("setUserLoggedIn", resp.data);
      });
    },
  },
  modules: {},
});
