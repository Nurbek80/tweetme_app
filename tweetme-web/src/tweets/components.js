import React, {useEffect, useRef, useState}from "react";
import { apiTweetCreate, apiTweetList, apiTweetAction } from "./lookup";


export function TweetsComponent(props) {
    const textAreaRef = useRef()
    const [newTweets, setNewTweets] = useState([]) 
    const handleCallBack = (response, status) => {
        let tempNewTweets = [...newTweets]
        if(status === 201) {
            tempNewTweets.unshift(response)
            setNewTweets(tempNewTweets)
        } else {
            console.log(response)
            alert("Error Occured while creating tweet")
        }
    }
    const handleSubmit = (event) => {
        event.preventDefault()
        const newVal = textAreaRef.current.value
        apiTweetCreate(newVal, handleCallBack)
        textAreaRef.current.value = ''
    }
    return (
        <div className={props.className}>
            <div className="col-12 mb-3">
                <form onSubmit={handleSubmit}>
                    <textarea ref={textAreaRef} required={true} className="form-control" name="tweet">

                    </textarea>
                    <button type='submit' className="btn btn-primary my-3">Tweet</button>
                </form>
            </div>
            <TweetList newTweets={newTweets}/>
        </div>
    )
}

export function TweetList(props) {
    const [tweetsInit, setTweetsInit] = useState([])
    const [tweets, setTweets] = useState([])
    const [tweetsDidSet,setTweetsDidSet] = useState(false)
    
    useEffect(() => {
        const final = [...props.newTweets].concat(tweetsInit)
        if(final.length !== tweets.length) {
            setTweets(final)
        }
    },[props.newTweets, tweets, tweetsInit])
    useEffect(() => {
        if(tweetsDidSet === false) {
            const myCallBack = (response, status) => {
                console.log(response, status)
                if(status === 200) {
                    setTweetsInit(response)
                    setTweetsDidSet(true)
                }
                else alert("There was an Error....")
            } 
            apiTweetList(myCallBack)
        }
    },[tweetsDidSet])
    return (
      <div>
        {tweets.map((item, index) => {
          return <Tweet tweet={item} className='my-5 py-5 border bg-white text-dark'key={`${index}-${item.id}`} />
        })}
      </div>
    )
}

export function ActionBtn(props) {

    const {tweet, action} = props
    const [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0)
    //const [userLike, setUserLike] = useState(tweet.userLike === true ? true: false)
    const className = props.className ? props.className:'btn btn-primary btn-sm'
    
    const handleBackendActionEvent = (response, status) => {
        console.log(response, status)
        if(status === 200) {
            setLikes(response.likes)
            //setUserLike(true)
        }
    }
    const handleClick = (event) => {
        event.preventDefault()
        apiTweetAction(tweet.id, action.type, handleBackendActionEvent,)
        
    }
    const display = action.type === 'like' ? `${likes} ${action.display}` : action.display
    return <button className={className} onClick={handleClick}>{display}</button> 
}
  
export function Tweet(props) {
    
    const {tweet} = props
    const className = props.className ? props.className:'col-10 mx-auto col-md-6'
    return (
      <div className={className}>
        <p>{tweet.id}-{tweet.content}</p>
        <div className='btn btn-group'>
          <ActionBtn tweet={tweet} action={{type: "like", display: "Like"}}/>
          <ActionBtn tweet={tweet} action={{type: "unlike", display: "UnLike"}}/>
          <ActionBtn tweet={tweet} action={{type: "retweet", display: "Retweet"}}/>
        </div>
      </div>
    )
}


