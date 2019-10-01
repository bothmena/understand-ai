# entry point for the application
from pubsub import pub

from event_dispatcher import dispatch
from eventlistener import OnFrameAddedEventListener, OnBoxCreatedEventListener, OnBoxDeletedEventListener, \
    OnEndOfStreamEventListener, OnBoxMovedEventListener, OnBoxAttributeChangedEventListener, OnExtractBoxEventListener, OnClassifyTrafficLightEventListener
from utils.constants import Topics

# instantiate the event listeners
on_frame_added = OnFrameAddedEventListener()
on_box_created = OnBoxCreatedEventListener()
on_box_deleted = OnBoxDeletedEventListener()
on_box_moved = OnBoxMovedEventListener()
on_box_att_changed = OnBoxAttributeChangedEventListener()
on_end_of_stream = OnEndOfStreamEventListener()
on_extract_box = OnExtractBoxEventListener()
on_classify_tl = OnClassifyTrafficLightEventListener()

# make each event listener subscribe to its event.
pub.subscribe(on_frame_added.handle, Topics.FRAME_ADDED)
pub.subscribe(on_box_created.handle, Topics.BOX_CREATED)
pub.subscribe(on_box_deleted.handle, Topics.BOX_DELETED)
pub.subscribe(on_box_moved.handle, Topics.BOX_MOVED)
pub.subscribe(on_box_att_changed.handle, Topics.BOX_ATTRIBUTE_CHANGED)
pub.subscribe(on_end_of_stream.handle, Topics.END_OF_STREAM)
pub.subscribe(on_extract_box.handle, Topics.EXTRACT_BOX)
pub.subscribe(on_classify_tl.handle, Topics.CLASSIFY_TRAFFIC_LIGHT)

dispatch('var/input/events.csv')
