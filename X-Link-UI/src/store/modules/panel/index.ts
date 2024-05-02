import { defineStore } from 'pinia'
import { defaultState, defaultStatePanelConfig, getLocalState, removeLocalState, setLocalState } from './helper'
import { router } from '@/router'
import type { PanelStateNetworkModeEnum } from '@/enums'
import { get as getUserConfig } from '@/api/panel/userConfig'
export const usePanelState = defineStore('panel', {
  state: (): Panel.State => getLocalState() || defaultState(),

  getters: {

  },

  actions: {
    setLeftSiderCollapsed(Collapsed: boolean) {
      this.leftSiderCollapsed = Collapsed
      // this.recordState()
    },

    setRightSiderCollapsed(Collapsed: boolean) {
      this.rightSiderCollapsed = Collapsed
      // this.recordState()
    },

    setNetworkMode(mode: PanelStateNetworkModeEnum) {
      this.networkMode = mode
      this.recordState()
    },

    // 获取云端（搭建的服务器）的面板配置
    updatePanelConfigByCloud() {
      getUserConfig<Panel.userConfig>().then((res) => {
        if (res.code === 0)
          this.panelConfig = { ...defaultStatePanelConfig(), ...res.data.panel }
        else
          this.resetPanelConfig() // 重置恢复默认
        this.recordState()
      })
    },

    resetPanelConfig() {
      this.panelConfig = defaultStatePanelConfig()
    },

    // async refreshSpaceNoteList(spaceId: string) {
    //   await getListBySpaceNoteId<Common.ListResponse<SNote.InfoTree[]>>(spaceId).then((res) => {
    //     this.notesList = res.data.list
    //   })
    // },

    async reloadRoute(id?: number) {
      // this.recordState()
      await router.push({ name: 'AppletDialog', params: { aiAppletId: id } })
    },

    recordState() {
      setLocalState(this.$state)
    },

    removeState() {
      removeLocalState()
    },
  },
})
