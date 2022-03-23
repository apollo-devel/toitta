import axios from "axios";
import UIkit from "uikit";
import { createStore } from "vuex";

import router from "@/router";

function defaultErrorHandler(error) {
  if (error.response.status === 401) {
    router.push("/login");
  } else {
    UIkit.notification(error.response.data.error.message, {
      status: "danger",
    });
  }
}

export default createStore({
  state: {
    userLoggedIn: undefined,
    posts: [],
    profile: {
      user: {
        display_name: "",
        username: "",
      },
      users: [],
    },
    replyTo: undefined,
  },
  getters: {},
  mutations: {
    setUserLoggedIn(state, args) {
      state.userLoggedIn = args.user;
    },
    setPosts(state, args) {
      state.posts = args.posts;
    },
    prependPost(state, args) {
      state.posts.unshift(args.post);
    },
    updatePost(state, args) {
      const orig = state.posts.find((p) => p._id === args.post._id);
      if (orig) {
        Object.assign(orig, args.post);
      }
      state.posts
        .filter(
          (p) => p.retweeted_post && p.retweeted_post._id === args.post._id
        )
        .forEach((p) => Object.assign(p.retweeted_post, args.post));
    },
    setProfileUser(state, args) {
      state.profile.user = args.user;
    },
    setProfileUsers(state, args) {
      state.profile.users = args.users;
    },
    setReplyTo(state, args) {
      state.replyTo = args.post;
    },
  },
  actions: {
    async registerUser({ commit }, args) {
      return axios.post("/api/users", args.user).then((resp) => {
        commit("setUserLoggedIn", { user: resp.data });
      });
    },
    async login({ commit }, args) {
      return axios.post("/api/login", args.credential).then((resp) => {
        commit("setUserLoggedIn", { user: resp.data });
      });
    },
    async logout({ commit }) {
      return axios.post("/api/logout").then(() => {
        commit("setUserLoggedIn", { user: undefined });
      });
    },
    async loginCheck({ commit }) {
      return axios.get("/api/session").then((resp) => {
        commit("setUserLoggedIn", { user: resp.data });
      });
    },
    async createPost({ commit, state }, args) {
      const body = {
        content: args.content,
        posted_by: state.userLoggedIn._id,
      };
      if (args.reply_to) {
        body.reply_to = args.reply_to;
      }
      return axios.post("/api/posts", body).then((resp) => {
        commit("prependPost", { post: resp.data });
        if (resp.data.reply_to) {
          // 返信を投稿した場合は返信先の返信件数の表示を更新する
          commit("updatePost", { post: resp.data.reply_to });
        }
      });
    },
    async loadPosts({ commit }) {
      return axios
        .get("/api/posts")
        .then((resp) => {
          commit("setPosts", { posts: resp.data });
        })
        .catch(defaultErrorHandler);
    },
    async likePost({ commit }, args) {
      return axios
        .post(`/api/posts/${args.post._id}/like`)
        .then((resp) => {
          commit("updatePost", { post: resp.data });
        })
        .catch(defaultErrorHandler);
    },
    async unlikePost({ commit }, args) {
      return axios
        .delete(`/api/posts/${args.post._id}/like`)
        .then((resp) => {
          commit("updatePost", { post: resp.data });
        })
        .catch(defaultErrorHandler);
    },
    async retweetPost({ commit }, args) {
      return axios
        .post(`/api/posts/${args.post._id}/retweet`)
        .then((resp) => {
          commit("updatePost", { post: resp.data });
        })
        .catch(defaultErrorHandler);
    },
    async unretweetPost({ commit }, args) {
      return axios
        .delete(`/api/posts/${args.post._id}/retweet`)
        .then((resp) => {
          commit("updatePost", { post: resp.data });
        })
        .catch(defaultErrorHandler);
    },
    async loadProfileUser({ commit }, args) {
      return axios
        .get(`/api/users/${args.username}`)
        .then((resp) => {
          commit("setProfileUser", { user: resp.data });
        })
        .catch(defaultErrorHandler);
    },
    async followUser({ commit }, args) {
      return axios
        .post(`/api/users/${args.username}/follow`)
        .then((resp) => {
          commit("setUserLoggedIn", { user: resp.data });
        })
        .catch(defaultErrorHandler);
    },
    async unfollowUser({ commit }, args) {
      return axios
        .delete(`/api/users/${args.username}/follow`)
        .then((resp) => {
          commit("setUserLoggedIn", { user: resp.data });
        })
        .catch(defaultErrorHandler);
    },
    async loadFollowers({ commit }, args) {
      return axios
        .get(`/api/users/${args.username}/followers`)
        .then((resp) => {
          commit("setProfileUsers", { users: resp.data });
        })
        .catch(defaultErrorHandler);
    },
    async loadFollowingUsers({ commit }, args) {
      return axios
        .get(`/api/users/${args.username}/following`)
        .then((resp) => {
          commit("setProfileUsers", { users: resp.data });
        })
        .catch(defaultErrorHandler);
    },
    async openReplyModal({ commit }, args) {
      return commit("setReplyTo", { post: args.post });
    },
  },
  modules: {},
});
