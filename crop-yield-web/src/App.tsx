import { useState } from 'react'
import { predictCropYield, predictCropYieldAdvice } from './data-access/predict-crop-yield'
import { PredictCropYieldRequest, PredictCropYieldResponse, PredictCropYieldAdviceResponse } from './data/predict-crop-yield'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Loader2 } from 'lucide-react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function CropYieldPrediction() {
  const [formData, setFormData] = useState<PredictCropYieldRequest>({
    land_area: '1000',
    rainfall: 'normal',
    disease_level: 'normal',
    temperature: '21.8',
    planting_distance: '20cmx20cm'
  })

  const [prediction, setPrediction] = useState<PredictCropYieldResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [advice, setAdvice] = useState<PredictCropYieldAdviceResponse | null>(null)
  const [showModal, setShowModal] = useState(false)

  const handleChange = (name: string, value: string) => {
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)
    try {
      const yieldPrediction = await predictCropYield(formData)
      setPrediction(yieldPrediction)
      console.log('Predicted Crop Yield:', yieldPrediction)
    } catch (error) {
      console.error('Error predicting crop yield:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleGetAdvice = async () => {
    if (prediction) {
      try {
        const adviceResponse = await predictCropYieldAdvice(prediction)
        setAdvice(adviceResponse)
        setShowModal(true)
      } catch (error) {
        console.error('Error getting crop yield advice:', error)
      }
    }
  }

  return (
    <div className="h-screen flex items-center justify-center">
      <div className="container mx-auto py-10 bg-background text-foreground flex lg:flex-row flex-col lg:gap-10 lg:justify-center">
        <form onSubmit={handleSubmit}>
          <Card className="max-w-2xl mx-auto lg:mx-0">
            <CardHeader>
              <CardTitle className="text-primary">Prediksi Hasil Panen</CardTitle>
              <CardDescription>Masukkan data untuk memprediksi hasil panen Anda.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="land_area">Land Area</Label>
                  <Input
                    id="land_area"
                    type="number"
                    value={formData.land_area}
                    onChange={(e) => handleChange('land_area', e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="rainfall">Rainfall</Label>
                  <Select value={formData.rainfall} onValueChange={(value: string) => handleChange('rainfall', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select rainfall level" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="sangat rendah">Sangat Rendah</SelectItem>
                      <SelectItem value="rendah">Rendah</SelectItem>
                      <SelectItem value="normal">Normal</SelectItem>
                      <SelectItem value="tinggi">Tinggi</SelectItem>
                      <SelectItem value="sangat tinggi">Sangat Tinggi</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="disease_level">Disease Level</Label>
                  <Select value={formData.disease_level} onValueChange={(value: string) => handleChange('disease_level', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select disease level" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="sangat rendah">Sangat Rendah</SelectItem>
                      <SelectItem value="rendah">Rendah</SelectItem>
                      <SelectItem value="normal">Normal</SelectItem>
                      <SelectItem value="tinggi">Tinggi</SelectItem>
                      <SelectItem value="sangat tinggi">Sangat Tinggi</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="temperature">Temperature</Label>
                  <Input
                    id="temperature"
                    type="number"
                    step="0.1"
                    value={formData.temperature}
                    onChange={(e) => handleChange('temperature', e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="planting_distance">Planting Distance</Label>
                  <Select value={formData.planting_distance} onValueChange={(value: string) => handleChange('planting_distance', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select planting distance" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="20cmx20cm">20cm x 20cm</SelectItem>
                      <SelectItem value="25cmx25cm">25cm x 25cm</SelectItem>
                      <SelectItem value="30cmx30cm">30cm x 30cm</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
            <CardFooter>
              <Button type="submit" className="w-full bg-primary text-primary-foreground" disabled={loading}>
                {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
                {loading ? 'Memproses...' : 'Submit'}
              </Button>
            </CardFooter>
          </Card>
        </form>

        {prediction && (
          <>
            <Card className="mt-8 lg:mt-0 max-w-2xl mx-auto lg:mx-0">
              <CardHeader>
                <CardTitle className="text-primary">Hasil Prediksi</CardTitle>
              </CardHeader>
              <CardContent>
                <dl className="grid grid-cols-2 gap-4">
                  <div>
                    <dt className="font-medium text-secondary-foreground">Land Area</dt>
                    <dd><Badge>{prediction.land_area}</Badge></dd>
                  </div>
                  <div>
                    <dt className="font-medium text-secondary-foreground">Rainfall</dt>
                    <dd><Badge>{prediction.rainfall}</Badge></dd>
                  </div>
                  <div>
                    <dt className="font-medium text-secondary-foreground">Disease Level</dt>
                    <dd><Badge>{prediction.disease_level}</Badge></dd>
                  </div>
                  <div>
                    <dt className="font-medium text-secondary-foreground">Temperature</dt>
                    <dd><Badge>{prediction.temperature}</Badge></dd>
                  </div>
                  <div>
                    <dt className="font-medium text-secondary-foreground">Planting Distance</dt>
                    <dd><Badge>{prediction.planting_distance}</Badge></dd>
                  </div>
                  <div>
                    <dt className="font-medium text-secondary-foreground">Seed Weight</dt>
                    <dd><Badge>{prediction.seed_weight}</Badge></dd>
                  </div>
                  <div>
                    <dt className="font-medium text-secondary-foreground">GKP</dt>
                    <dd><Badge>{prediction.gkp}</Badge></dd>
                  </div>
                  <div>
                    <dt className="font-medium text-secondary-foreground">GKG</dt>
                    <dd><Badge>{prediction.gkg}</Badge></dd>
                  </div>
                  <div>
                    <dt className="font-medium text-secondary-foreground">Rice</dt>
                    <dd><Badge>{prediction.rice}</Badge></dd>
                  </div>
                </dl>
                <Button className="mt-4 w-full bg-secondary text-secondary-foreground" onClick={handleGetAdvice}>
                  Get Advice
                </Button>
              </CardContent>
            </Card>

            {advice && (
              <Dialog open={showModal} onOpenChange={setShowModal}>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Advice</DialogTitle>
                  </DialogHeader>
                  <DialogContent>
                    <Markdown remarkPlugins={[remarkGfm]}>{advice.advice}</Markdown>
                  </DialogContent>
                  <DialogFooter>
                    <Button onClick={() => setShowModal(false)}>Close</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            )}
          </>
        )}
      </div>
    </div>
  )
}

