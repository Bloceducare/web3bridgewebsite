const getTrack = (trackUrl:string) => {
    if(!trackUrl) return [0, 0]
    const tr = trackUrl?.split('/')?.pop()?.split("?") ?? []
    const [track, type] = tr
    let sortType;
    if(type){
      sortType =  type.split("").slice(-1)
    }
      return [track, sortType?.[0]]
  }

  export default getTrack