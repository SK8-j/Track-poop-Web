import { createStore } from 'vuex';

const store = createStore({
  state: {
    // 在这里定义全局状态，例如：
    poopCount: 0,
  },
  mutations: {
    // 在这里定义变更状态的方法，例如：
    incrementPoop(state, count) {
      state.poopCount += count;
    },
  },
  actions: {
    // 异步操作或者复杂的逻辑可以在这里定义，例如：
    addPoop({ commit }, count) {
      commit('incrementPoop', count);
    },
  },
  getters: {
    // 获取状态的getter，例如：
    getPoopCount: (state) => state.poopCount,
  },
});

export default store;
