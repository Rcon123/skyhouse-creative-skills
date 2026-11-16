# Omnihuman 1.5

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/v1/jobs/createTask:
    post:
      summary: Omnihuman 1.5
      deprecated: false
      description: >-
        ## Create Task


        Use this endpoint to create a new audio-driven portrait animation task.
        Upload a portrait image and an audio file, and the model will generate a
        video of the subject speaking or moving in sync with the audio.


        <Card title="Get Task Details" icon="lucide-search"
        href="/market/common/get-task-detail">
          After submission, use the unified query endpoint to check task progress and retrieve results
        </Card>


        ::: tip[]

        For production use, we recommend providing the `callBackUrl` parameter
        so your service can receive completion notifications instead of polling
        for task status.

        :::


        ## File Upload


        ::: tip[]

        Need to upload files before calling this endpoint? See [File Upload API
        Quickstart](/file-upload-api/quickstart).

        :::


        ## Related Resources


        <CardGroup cols={2}>
          <Card title="Model Marketplace" icon="lucide-store" href="/market/quickstart">
            Explore all available models and capabilities
          </Card>
          <Card title="Common API" icon="lucide-cog" href="/common-api/get-account-credits">
            Check account credits and usage
          </Card>
        </CardGroup>
      operationId: omnihuman-1-5
      tags:
        - docs/en/Market/Video Models/OmniHuman
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required:
                - model
                - input
              properties:
                model:
                  type: string
                  enum:
                    - omnihuman-1-5
                  default: omnihuman-1-5
                  description: |-
                    The model name used for generation. This field is required.

                    - This endpoint must use the `omnihuman-1-5` model
                  examples:
                    - omnihuman-1-5
                input:
                  type: object
                  description: >-
                    Input parameters for the audio-driven portrait animation
                    task.
                  required:
                    - image_url
                    - audio_url
                  properties:
                    image_url:
                      type: string
                      format: uri
                      description: >-
                        Portrait image URL. Supports any aspect ratio with
                        subjects including people, pets, anime, etc. Accepted
                        file types: image/jpeg, image/png, image/webp. Max file
                        size: 10MB.
                    mask_url:
                      type: array
                      items:
                        type: string
                        format: uri
                      maxItems: 5
                      description: >-
                        Optional mask image URL(s). To have a specific subject
                        in the image speak, use 'Subject Detection' to get the
                        corresponding mask image and pass it as input. Accepted
                        file types: image/jpeg, image/png, image/webp. Max file
                        size: 10MB. Multiple file upload is supported, up to 5
                        files.
                    audio_url:
                      type: string
                      format: uri
                      description: >-
                        Audio URL. Duration must be less than 60 seconds
                        (recommended 15 seconds or less; exceeding this will
                        cause quality degradation). Accepted file types:
                        audio/mpeg, audio/wav, audio/x-wav, audio/aac,
                        audio/ogg, audio/mp4. Max file size: 10MB.
                    prompt:
                      type: string
                      description: >-
                        Optional prompt text. Limited to Chinese, English,
                        Japanese, Korean, Spanish, and Indonesian. Recommended
                        300 characters or less. Maximum length: 1000 characters.
                      maxLength: 300
                    output_resolution:
                      type: string
                      enum:
                        - '720'
                        - '1080'
                      default: '1080'
                      description: |-
                        Output video resolution.

                        - `720`: 720P
                        - `1080`: 1080P (default)
                    pe_fast_mode:
                      type: boolean
                      default: false
                      description: >-
                        Fast mode. Sacrifices some quality to speed up
                        generation. Default value: `false`.
                    seed:
                      type: integer
                      default: -1
                      description: >-
                        Random seed. Default is `-1` (random). When using the
                        same positive integer and keeping all other parameters
                        identical, the result will be highly consistent.
                  x-apidog-orders:
                    - image_url
                    - mask_url
                    - audio_url
                    - prompt
                    - output_resolution
                    - pe_fast_mode
                    - seed
                  x-apidog-ignore-properties: []
                callBackUrl:
                  type: string
                  format: uri
                  description: >-
                    Callback URL. Once the task is fully completed, kie will
                    send the result to the business webhook URL.
              x-apidog-orders:
                - model
                - input
                - callBackUrl
              x-apidog-ignore-properties: []
            example:
              model: omnihuman-1-5
              input:
                image_url: https://your-domain.com/image/portrait.png
                mask_url:
                  - https://your-domain.com/image/mask.png
                audio_url: https://your-domain.com/audio/speech.mp3
                prompt: A person speaking naturally with gentle expressions.
                output_resolution: '1080'
                pe_fast_mode: false
                seed: -1
              callBackUrl: https://your-domain.com/api/callback
      responses:
        '200':
          description: Request successful
          content:
            application/json:
              schema:
                allOf:
                  - type: object
                    properties:
                      code:
                        type: integer
                        description: >-
                          Response Status Codes


                          200: Success - The request was successfully processed.


                          401: Unauthorized - Insufficient or invalid
                          authentication credentials.


                          402: Insufficient Quota - The account has insufficient
                          quota to perform this operation.


                          404: Not Found - The requested resource or interface
                          does not exist.


                          422: Validation Error - The request parameters failed
                          the validation check.


                          429: Request Restricted - The request frequency limit
                          for this resource has been exceeded.


                          433: Request Limit - The subkey usage exceeded the
                          limit.


                          455: Service Unavailable - The system is currently
                          under maintenance.


                          500: Server Error - An unexpected error occurred while
                          processing the request.


                          501: Generation Failed - The content generation task
                          failed.


                          505: Feature Disabled - The requested feature is
                          currently disabled.
                        enum:
                          - 200
                          - 401
                          - 402
                          - 404
                          - 422
                          - 429
                          - 433
                          - 455
                          - 500
                          - 501
                          - 505
                      msg:
                        type: string
                        description: Response message, error description upon failure
                        examples:
                          - success
                      data:
                        type: object
                        required:
                          - taskId
                        properties:
                          taskId:
                            type: string
                            description: >-
                              The task ID can be used with the "Get Task
                              Details" endpoint to query the task status.
                            examples:
                              - dc1928bfcbc77cb6c85f3359a9c718b3
                        x-apidog-orders:
                          - taskId
                        x-apidog-ignore-properties: []
                    x-apidog-orders:
                      - 01KV7QY2EFNA3G5YVCSPGG8KCT
                    required:
                      - data
                    x-apidog-refs:
                      01KV7QY2EFNA3G5YVCSPGG8KCT:
                        $ref: '#/components/schemas/response%20not%20with%20recordId'
                    x-apidog-ignore-properties:
                      - code
                      - msg
                      - data
              example:
                code: 200
                msg: success
                data:
                  taskId: task_omnihuman-1-5_1234567890
          headers: {}
          x-apidog-name: ''
      security:
        - BearerAuth: []
          x-apidog:
            schemeGroups:
              - id: kn8M4YUlc5i0A0179ezwx
                schemeIds:
                  - BearerAuth
            required: true
            use:
              id: kn8M4YUlc5i0A0179ezwx
            scopes:
              kn8M4YUlc5i0A0179ezwx:
                BearerAuth: []
      callbacks:
        videoTaskCompleted:
          '{request.body#/callBackUrl}':
            post:
              description: >-
                The system sends this callback when the `omnihuman-1-5` task
                succeeds or fails.
              requestBody:
                required: true
                content:
                  application/json:
                    schema:
                      type: object
                      required:
                        - code
                        - msg
                        - data
                      properties:
                        code:
                          type: integer
                          description: >-
                            Unified callback code: 200 for success, 501 for
                            failure.
                          enum:
                            - 200
                            - 501
                        msg:
                          type: string
                          description: Unified callback message.
                          enum:
                            - Playground task completed successfully.
                            - Playground task failed.
                        data:
                          type: object
                          required:
                            - taskId
                            - model
                            - state
                            - param
                            - resultJson
                            - failCode
                            - failMsg
                          properties:
                            taskId:
                              type: string
                              description: The unique task identifier.
                            model:
                              type: string
                              description: The model used for the task.
                              enum:
                                - omnihuman-1-5
                            state:
                              type: string
                              description: Terminal task state.
                              enum:
                                - success
                                - fail
                            param:
                              type: string
                              description: >-
                                JSON string containing the submitted task
                                parameters.
                            resultJson:
                              type: string
                              nullable: true
                              description: >-
                                JSON string containing resultUrls,
                                firstFrameUrl, lastFrameUrl, or resultObject
                                when successful. Null when failed.
                            failCode:
                              type: string
                              nullable: true
                              description: Null when successful; failure code when failed.
                            failMsg:
                              type: string
                              nullable: true
                              description: >-
                                Null when successful; failure message when
                                failed.
                            costTime:
                              type: integer
                              format: int64
                              description: >-
                                Task processing time. Present on successful
                                callbacks.
                            completeTime:
                              type: integer
                              format: int64
                              description: Task completion timestamp.
                            createTime:
                              type: integer
                              format: int64
                              description: Task creation timestamp.
                            updateTime:
                              type: integer
                              format: int64
                              description: Task update timestamp.
                            creditsConsumed:
                              type: number
                              description: >-
                                Credits consumed by the task. Present on
                                successful callbacks.
                    examples:
                      success:
                        summary: Task completed successfully
                        value:
                          code: 200
                          msg: Playground task completed successfully.
                          data:
                            taskId: task_example_video_webhook_001
                            model: omnihuman-1-5
                            state: success
                            param: >-
                              {"input":"{\"image_url\":\"https://example.com/input-image.jpg\",\"mask_url\":[\"https://example.com/input-image.jpg\"],\"audio_url\":\"https://example.com/input-audio.mp3\",\"prompt\":\"A
                              person speaking naturally with gentle
                              expressions.\",\"output_resolution\":\"1080\",\"pe_fast_mode\":false,\"seed\":-1}","callBackUrl":"https://example.com/callback","model":"omnihuman-1-5"}
                            resultJson: >-
                              {"resultUrls":["https://example.com/generated-video.mp4"]}
                            failCode: null
                            failMsg: null
                            costTime: 12
                            completeTime: 1234567890
                            createTime: 1234560000
                            updateTime: 1234567890
                            creditsConsumed: 1.23
                      failure:
                        summary: Task failed
                        value:
                          code: 501
                          msg: Playground task failed.
                          data:
                            taskId: task_example_video_webhook_001
                            model: omnihuman-1-5
                            state: fail
                            param: >-
                              {"input":"{\"image_url\":\"https://example.com/input-image.jpg\",\"mask_url\":[\"https://example.com/input-image.jpg\"],\"audio_url\":\"https://example.com/input-audio.mp3\",\"prompt\":\"A
                              person speaking naturally with gentle
                              expressions.\",\"output_resolution\":\"1080\",\"pe_fast_mode\":false,\"seed\":-1}","callBackUrl":"https://example.com/callback","model":"omnihuman-1-5"}
                            failCode: GENERATION_FAILED
                            failMsg: The generation task failed.
              responses:
                '200':
                  description: Callback received successfully.
                  content:
                    application/json:
                      schema:
                        type: object
                        properties:
                          code:
                            type: integer
                            example: 200
                          msg:
                            type: string
                            example: success
                      example:
                        code: 200
                        msg: success
      x-apidog-folder: docs/en/Market/Video Models/OmniHuman
      x-apidog-status: released
      x-run-in-apidog: https://app.apidog.com/web/project/1184766/apis/api-37874920-run
components:
  schemas:
    response not with recordId:
      type: object
      required:
        - data
      properties:
        code:
          type: integer
          description: >-
            Response Status Codes


            200: Success - The request was successfully processed.


            401: Unauthorized - Insufficient or invalid authentication
            credentials.


            402: Insufficient Quota - The account has insufficient quota to
            perform this operation.


            404: Not Found - The requested resource or interface does not exist.


            422: Validation Error - The request parameters failed the validation
            check.


            429: Request Restricted - The request frequency limit for this
            resource has been exceeded.


            433: Request Limit - The subkey usage exceeded the limit.


            455: Service Unavailable - The system is currently under
            maintenance.


            500: Server Error - An unexpected error occurred while processing
            the request.


            501: Generation Failed - The content generation task failed.


            505: Feature Disabled - The requested feature is currently disabled.
          enum:
            - 200
            - 401
            - 402
            - 404
            - 422
            - 429
            - 433
            - 455
            - 500
            - 501
            - 505
        msg:
          type: string
          description: Response message, error description upon failure
          examples:
            - success
        data:
          type: object
          required:
            - taskId
          properties:
            taskId:
              type: string
              description: >-
                The task ID can be used with the "Get Task Details" endpoint to
                query the task status.
              examples:
                - dc1928bfcbc77cb6c85f3359a9c718b3
          x-apidog-orders:
            - taskId
          x-apidog-ignore-properties: []
      x-apidog-orders:
        - code
        - msg
        - data
      x-apidog-ignore-properties: []
      x-apidog-folder: ''
  securitySchemes:
    BearerAuth:
      type: bearer
      scheme: bearer
      bearerFormat: API Key
      description: >-
        All API requests require a Bearer Token. Add the header `Authorization:
        Bearer YOUR_API_KEY` to authenticate requests.
    BearerAuth1:
      type: bearer
      scheme: bearer
      bearerFormat: API Key
      description: >-
        所有 API 请求都需要 Bearer Token。请在请求头中添加 `Authorization: Bearer YOUR_API_KEY`
        进行身份验证。
servers:
  - url: https://api.kie.ai
    description: 正式环境
security:
  - BearerAuth: []
    x-apidog:
      schemeGroups:
        - id: kn8M4YUlc5i0A0179ezwx
          schemeIds:
            - BearerAuth
      required: true
      use:
        id: kn8M4YUlc5i0A0179ezwx
      scopes:
        kn8M4YUlc5i0A0179ezwx:
          BearerAuth: []

```
