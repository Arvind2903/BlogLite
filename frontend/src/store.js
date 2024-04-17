import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

export default new Vuex.Store({
  state : {
    user : null,
    token : null
  },
  mutations:{
    setUser(state, user){
      state.user = user;
      localStorage.setItem('user', JSON.stringify(user))
    },
    setToken(state, token){
      state.token = token;
      localStorage.setItem('token', token)
    }
  },
  actions:{},
  getters:{},
})