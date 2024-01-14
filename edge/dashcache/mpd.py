from typing import List, Literal, Dict


class MPD(object):
    def __init__(self,
                 content: str,
                 url: str,
                 type_: Literal["static", "dynamic"],
                 media_presentation_duration: float,
                 max_segment_duration: float,
                 adaptation_sets: Dict[int, 'AdaptationSet']
                 ):
        self.content = content
        """
        The raw content of the MPD file
        """

        self.url = url
        """
        The URL of the MPD file
        """

        self.type: Literal["static", "dynamic"] = type_
        """
        If this source is VOD ("static") or Live ("dynamic")
        """

        self.media_presentation_duration = media_presentation_duration
        """
        The media presentation duration in seconds
        """

        self.adaptation_sets: Dict[int, AdaptationSet] = adaptation_sets
        """
        All the adaptation sets
        """


class AdaptationSet(object):
    def __init__(self,
                 adaptation_set_id: int,
                 content_type: Literal["video", "audio"],
                 frame_rate: str,
                 max_width: int,
                 max_height: int,
                 par: str,
                 representations: Dict[int, 'Representation'],
                 segment_template: 'SegmentTemplate'
                 ):
        self.id = adaptation_set_id
        """
        The adaptation set id
        """

        self.content_type: str = content_type
        """
        The content type of the adaptation set. It could only be "video" or "audio"
        """

        self.frame_rate: str = frame_rate
        """
        The frame rate string
        """

        self.max_width: int = max_width
        """
        The maximum width
        """

        self.max_height: int = max_height
        """
        The maximum height
        """

        self.par: str = par
        """
        The ratio of width / height
        """

        self.representations: Dict[int, Representation] = representations
        """
        All the representations under the adaptation set
        """

        self.segment_template: SegmentTemplate = segment_template
        """
        All the Segment templates
        """


class Representation(object):
    def __init__(self, id_: str, mime_type: str,
                 codecs: str, bandwidth: int, width: int, height: int,
                 initialization: str, segments: List['Segment']):
        self.id = id_
        """
        The id of the representation
        """

        self.mime_type = mime_type
        """
        The mime type of the representation
        """

        self.codecs: str = codecs
        """
        The codec string of the representation
        """

        self.bandwidth: int = bandwidth
        """
        Average bitrate of this stream in bps
        """

        self.width = width
        """
        Width of picture
        """

        self.height = height
        """
        Height of picture
        """

        self.initialization: str = initialization
        """
        The initialization URL
        """

        self.segments: List[Segment] = segments
        """
        The video segments
        """


class SegmentTemplate(object):
    def __init__(self, duration: float, timescale: float, media: str, startNumber: int, initialization: str):
        self.duration = duration,
        """
        The duration of the segment in seconds
        """

        self.timescale = timescale,
        """
        Attribute to determine the segment duration
        Segment duration = Duration ÷ Timescale
        """

        self.media = media,
        """
        Defines the URL where playback devices send segment requests
        """

        self.startNumber = startNumber,
        """
        Indicates the starting number of the segment sequence
        """

        self.initialization = initialization
        """
        URL template for the initialization segment
        """


class Segment(object):
    def __init__(self, url: str, duration: float):
        self.url = url
        """
        The complete url of the segment
        """

        self.duration = duration
        """
        The duration of the segment in seconds
        """
