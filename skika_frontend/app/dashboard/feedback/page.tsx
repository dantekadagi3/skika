"use client"

import useSWR from "swr"
import { apiClient } from "@/lib/api-client"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { StarIcon } from "lucide-react"
import SentimentAnalyzer from "@/components/feedback/sentiment-analyzer"

interface Feedback {
  id: string
  report: string
  citizen: string
  rating: number
  comment: string
  created_at: string
}

export default function FeedbackPage() {
  const { data: feedback, isLoading } = useSWR<any>("/feedback/", (endpoint: string) => apiClient.get(endpoint))

  // Normalize API response to always be an array. Backend may return
  // { results: [...] } or { data: [...] } or the array directly.
  const feedbackArray: Feedback[] = Array.isArray(feedback)
    ? feedback
    : feedback && (Array.isArray(feedback.results) || Array.isArray(feedback.data))
    ? (feedback.results ?? feedback.data)
    : []

  const avgRating = feedbackArray.length
    ? (feedbackArray.reduce((sum, f) => sum + f.rating, 0) / feedbackArray.length).toFixed(1)
    : 0

  const ratingDistribution =
    feedbackArray.reduce(
      (acc, f) => {
        acc[f.rating] = (acc[f.rating] || 0) + 1
        return acc
      },
      {} as Record<number, number>,
    ) || {}

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground dark:text-foreground-dark">Citizen Feedback</h1>
        <p className="text-foreground-muted dark:text-foreground-dark-muted mt-2">
          Reviews, ratings, and sentiment analysis
        </p>
      </div>

  {/* Sentiment Analysis Section */}
  {feedbackArray && feedbackArray.length > 0 && <SentimentAnalyzer feedback={feedbackArray} />}

      {/* Rating Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Average Rating
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">{avgRating}</div>
            <div className="flex gap-1 mt-1">
              {[...Array(5)].map((_, i) => (
                <StarIcon
                  key={i}
                  className={`w-4 h-4 ${
                    i < Math.round(Number.parseFloat(avgRating as string))
                      ? "fill-yellow-400 text-yellow-400"
                      : "text-gray-300"
                  }`}
                />
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Total Reviews
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">{feedback?.length || 0}</div>
            <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">Citizen submissions</p>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Positive (4-5 stars)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600 dark:text-green-400">
              {feedbackArray.filter((f) => f.rating >= 4).length || 0}
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Satisfaction Rate
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
              {feedbackArray.length ? Math.round((feedbackArray.filter((f) => f.rating >= 4).length / feedbackArray.length) * 100) : 0}%
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Rating Distribution */}
      <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
        <CardHeader>
          <CardTitle>Rating Distribution</CardTitle>
          <CardDescription>Breakdown of ratings</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[5, 4, 3, 2, 1].map((stars) => {
              const count = ratingDistribution[stars] || 0
              const percentage = feedbackArray.length ? (count / feedbackArray.length) * 100 : 0

              return (
                <div key={stars}>
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-sm font-medium text-foreground dark:text-foreground-dark min-w-12">
                      {stars} ⭐
                    </span>
                    <div className="flex-1 bg-border dark:bg-border-dark rounded-full h-2">
                      <div
                        className="bg-yellow-400 h-2 rounded-full transition-all"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-foreground-muted dark:text-foreground-dark-muted min-w-12 text-right">
                      {count}
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Recent Feedback */}
      <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
        <CardHeader>
          <CardTitle>Recent Feedback</CardTitle>
          <CardDescription>Latest citizen reviews</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : feedbackArray && feedbackArray.length > 0 ? (
            <div className="space-y-4">
              {feedbackArray.map((item) => (
                <div key={item.id} className="border border-border dark:border-border-dark rounded-lg p-4">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex gap-1">
                      {[...Array(5)].map((_, i) => (
                        <StarIcon
                          key={i}
                          className={`w-4 h-4 ${i < item.rating ? "fill-yellow-400 text-yellow-400" : "text-gray-300"}`}
                        />
                      ))}
                    </div>
                    <span className="text-xs text-foreground-muted dark:text-foreground-dark-muted">
                      {new Date(item.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-sm text-foreground dark:text-foreground-dark">{item.comment}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-foreground-muted dark:text-foreground-dark-muted">
              No feedback available
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
