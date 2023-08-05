"""
quote.py
-----------

Create a new remote Quote using CAD files, or access an
existing one referenced by quoteId.

The most recent generated REST API documentation is available at:
https://api.kerfed.com/docs/v1
"""

import os

# requests is the only non-stdlib dependency
import requests


class _Quote(object):
    """
    The base class for a Quote object.
    """

    def __init__(self,
                 file_obj=None,
                 file_type=None,
                 quoteId=None,
                 shopId=None):
        """
        Create a new Quote or query one remotely.

        Parameters
        ----------
        file_obj : None or str
          File name to start quote with.
        file_type : None or str
          Type of file if not filename.
        quoteId : None or str
          If not None will access existing quote.
        shopId : None or str
          If not None will set the shopId on the new quote.
        """

        # create a session containing the API key
        self._session = requests.Session()
        self._session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self._API_KEY})

        # if not passed set the default shop here
        if shopId is None:
            shopId = 'kerfed'

        # if no quoteId was passed create a new one
        if quoteId is None:
            response = self._session.post(
                '{}/quotes'.format(self._API_ROOT),
                params={"timeout": self._TIMEOUT},
                json={'shopId': shopId})
            if not response.ok:
                raise ValueError(response.text)
            # save the quote ID
            self.quoteId = response.json()['id']
        else:
            # save the passed quoteId
            self.quoteId = quoteId

        # add a file if passed
        self.add_file(file_obj=file_obj,
                      file_type=file_type)

    def add_file(self, file_obj, file_type=None):
        """
        Add a CAD file to the quote which will be processed
        automatically.

        Parameters
        -----------
        file_obj : None or str
          File to upload to the Kerfed Engine.
        file_type : None or str
          Type of file if not a filename.
        """
        if file_obj is None:
            return

        # this is the remote filename
        FILENAME = os.path.split(file_obj)[-1]
        # we are always going to set the content type
        CONTENT_TYPE = 'application/octet-stream'

        # Request a signed URL to upload the file.
        # We specify our desired filename here.
        upload_response = self._session.post(
            '{}/uploads'.format(self._API_ROOT),
            json={"filename": FILENAME,
                  "contentType": CONTENT_TYPE})

        # before getting JSON raise if we failed
        if not upload_response.ok:
            raise ValueError(upload_response.text)
        upload = upload_response.json()

        # get the path of the file on the file system
        path = os.path.abspath(
            os.path.expanduser(file_obj))

        # do the actual upload to the blobstore
        with open(path, 'rb') as f:
            blob_response = requests.put(
                upload['url'],
                data=f.read(),
                headers={
                    # this header must EXACTLY match the
                    # originally provided filename.
                    'x-goog-meta-filename': FILENAME,
                    'Content-Type': CONTENT_TYPE})
        # raise error if blob upload failed
        if not blob_response.ok:
            raise ValueError(blob_response.text)
        # now that the upload has been completed add it to the quote.
        response = self._session.post(
            '{root}/quotes/{quoteId}/files'.format(
                root=self._API_ROOT, quoteId=self.quoteId),
            json={"uploadId": upload['id']})
        # raise if we failed to add upload to quote
        if not response.ok:
            raise ValueError(response.text)

    @property
    def info(self):
        """
        Get the basic information about the quote.

        Returns
        ---------
        info : dict
          Includes shopId, id, etc.
        """
        response = self._session.get(
            '{root}/quotes/{quoteId}'.format(
                root=self._API_ROOT, quoteId=self.quoteId))
        if not response.ok:
            raise ValueError(response.text)

        return response.json()

    @property
    def files(self):
        """
        Get a list of files attached to this quote.

        Returns
        ---------
        files : list
          List of dict with file information.
        """
        response = self._session.get(
            '{root}/quotes/{quoteId}/files'.format(
                root=self._API_ROOT, quoteId=self.quoteId))
        if not response.ok:
            raise ValueError(response.text)
        # TODO : check out lazy iteration
        blob = response.json()
        return blob['items']

    @property
    def parts(self):
        """
        Get manufacturing analysis and prices for unique parts
        attached to this quote.

        Returns
        ----------
        parts : dict
          Keyed by partId
        """
        response = self._session.get(
            '{root}/quotes/{quoteId}/parts'.format(
                root=self._API_ROOT, quoteId=self.quoteId))
        if not response.ok:
            raise ValueError(response.text)
        # TODO : check out lazy iteration
        blob = response.json()
        return blob['items']

    def show(self):
        """
        Show the files in the quote using optional trimesh loader.
        """
        import trimesh
        for info in self.files:
            trimesh.load_remote(info['previews']['glb']).show()

    def shared_link(self, expiration=None):
        """
        Get a shared link to the current Quote.

        Parameters
        ----------
        expiration : None or int
          Expiration duration in seconds

        Returns
        --------
        link : str
          URL to a shared link containing Quote.
        """
        if expiration is None:
            # if not set use one day
            expiration = 24 * 60 * 60

        response = self._session.post(
            '{root}/quotes/{quoteId}/share'.format(
                root=self._API_ROOT, quoteId=self.quoteId),
            json={"expiration": expiration})

        if not response.ok:
            raise ValueError(response.text)
        # TODO : check out lazy iteration
        blob = response.json()
        return blob['link']

    @property
    def default_options(self):
        defaults = {part['id']: part['methods'][
            part['defaults']['options']['methodId']]['defaults']['options']
            for part in self.parts}
        return defaults

    def order(self, expediteId=None, discountId=None):
        """
        Convert this quote into an order.
        """
        if expediteId is None:
            expediteId = 'standard'

        response = self._session.post(
            '{root}/orders'.format(root=self._API_ROOT),
            json={"quoteId": self.quoteId,
                  'expediteId': expediteId,
                  'parts': self.default_options})
        if not response.ok:
            raise ValueError(response.text)
        # TODO : check out lazy iteration
        blob = response.json()

        if len(blob) <= 3 and 'items' in blob:
            orderId = blob['items'][-1]['id']
        else:
            orderId = blob['id']

        return self._ORDER(orderId=orderId)
